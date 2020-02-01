from django.core.management.base import BaseCommand

import mwparserfromhell as mwp

import urllib.request
import urllib.parse
import typing
import json
import re

from takanon.models import Clause, Section, Chapter


class TakanonWikiParser:
    def __init__(self, stdout, wiki_source: str):
        self.stdout = stdout

        self.clauses = []
        self.sections = []
        self.chapters = []

        self.curr_section = None
        self.curr_chapter = None

        self.lines_iter = iter(wiki_source.splitlines())

        while True:
            line_template, line = self._next_line()
            if line is None:
                break

            # At the top level, we expect each line to begin with a template
            if not line_template:
                continue

            if line_template.name == 'ח:סעיף':
                self._parse_clause(line_template)
            elif line_template.name == 'ח:קטע1':
                # {{ח:קטע1|חלק א|חלק א׳: הגדרות ופרשנות|תיקון: תש״ע, תשע״ב־3}}
                self.curr_section = {
                    'ordinal': str(line_template.params[0]),
                    'name': str(line_template.params[1])
                }
                
                self.sections.append(self.curr_section)
            elif line_template.name == 'ח:קטע2':
                # {{ח:קטע2|חלק ב פרק 3|פרק שלישי: חברי הכנסת|תיקון: תש״ע־2}}
                if not self.curr_section:
                    continue

                self.curr_chapter = {
                    'ordinal': str(line_template.params[0]),
                    'name': str(line_template.params[1]),
                    'section_ordinal': self.curr_section['ordinal']
                }

                self.chapters.append(self.curr_chapter)
        
    def _parse_clause(self, clause_template: mwp.nodes.Template):
        curr_chapter_ord = self.curr_chapter['ordinal'] if self.curr_chapter else None
        clause = {
            'number': str(clause_template.params[0]),
            'name': self._clean_line(clause_template.params[1].value),
            'chapter_ordinal': curr_chapter_ord
        }
        
        self.stdout.write(f"Parsing clause {clause['number']}: {clause['name']}")

        # Parse the sub-clauses, and build a JSON string with the clause body,
        # broken down.
        body = { 't': '', 'sub': [] }
        
        curr_subclause = body
        subclause_stack = []
        curr_depth = 0

        while True:
            line_template, line = self._next_line()
            if not line:
                # All clauses end with an empty line AFAIK
                break

            m = None
            if line_template:
                m = re.match(r'ח:(ת+)', str(line_template.name))
            
            if not m:
                # This just adds to the text of the current subclause
                curr_subclause['t'] += self._clean_line(line)
            else:
                # The number of ת characters determines the nesting depth
                # of the sub section:
                depth = len(m.group(1))
                if depth == 1:
                    # Not a subclause, but the text of the clause itself
                    # {{ח:ת}} ואלו הן הוועדות הקבועות ותחומי עניניהן:
                    body['t'] += self._clean_line(line)
                    continue

                # Depending on the number of parameters to the leading template
                # it can create more than one subclause at once (or none at all)
                num_args = len(line_template.params)
                assert num_args in (1, 2)

                temp_parent = None
                if num_args == 1:
                    new_subclause = {
                        'n': str(line_template.params[0]),
                        't': self._clean_line(line),
                        'sub': []
                    }
                    next_depth = depth
                elif num_args == 2:
                    # Subclause with no text of its' own, just has sub-subclauses
                    # {ח:תת|(ב)|(1)}} ועדה ....
                    new_subclause = {
                        'n': str(line_template.params[1]),
                        't': self._clean_line(line),
                        'sub': []
                    }
                    temp_parent = {
                        'n': str(line_template.params[0]),
                        'sub': [new_subclause]
                    }
                    next_depth = depth + 1

                if depth > curr_depth:
                    parent = curr_subclause    
                    subclause_stack.append(curr_subclause)
                else:
                    if depth < curr_depth:
                        subclause_stack.pop()
                    
                    parent = subclause_stack[-1]

                if temp_parent:
                    subclause_stack.append(temp_parent)
                    parent['sub'].append(temp_parent)
                else:
                    parent['sub'].append(new_subclause)

                curr_subclause = new_subclause
                curr_depth = next_depth

        clause['clause_text'] = json.dumps(
            body,
            indent=2,
            ensure_ascii=False)
        self.clauses.append(clause)
        
    def _next_line(self) -> typing.Tuple[mwp.nodes.Template, mwp.wikicode.Wikicode]:
        """
        Get the next line in the source, parsed from WikiText,
        as a pair of its' first template and the entire line.
        """
        line = next(self.lines_iter, None)
        if line is None:
            return (None, None)
        
        parsed_line = mwp.parse(line)
        templates = parsed_line.filter_templates()

        first_template = templates[0] if templates else None
        return (first_template, parsed_line)        

    def _clean_line(self, val: mwp.wikicode.Wikicode) -> str:
        """
        Transforms a line in parsed WikiCode 
        """
        def map_node(node):
            if isinstance(node, mwp.nodes.Template):
                if node.name in ('ח:חיצוני', 'ח:פנימי'):
                    # {{ח:חיצוני|חוק-יסוד: הכנסת#סעיף 40|סעיף 40 לחוק־יסוד: הכנסת}}
                    # {{ח:פנימי|חלק ו|חלק ו׳}}
                    return node.params[1]
                elif node.name == 'ח:הערה':
                    # {{ח:הערה|(בוטל).}}
                    return node.params[0]
                else:
                    return ''
            else:
                return node.__strip__()
        
        return ''.join(str(map_node(n)) for n in val.nodes)


class Command(BaseCommand):
    help = 'Fetch the Knesset Takanon from WikiText'

    def add_arguments(self, arg_parser):
        arg_parser.add_argument(
            '--save-sources',
            action='store_true',
            help='Save source WikiText in the current working directory')

    def handle(self, *args, **kwargs):
        takanon_source = self._fetch_takanon_wikitext(kwargs['save_sources'])

        parser = TakanonWikiParser(self.stdout, takanon_source)

        self.stdout.write("Merging into database")
        section_entities = {}
        for section in parser.sections:
            entity, _ = Section.objects.update_or_create(
                ordinal=section['ordinal'],
                defaults={
                    'name': section['name']
                }
            )
            section_entities[section['ordinal']] = entity

        chapter_entities = {}
        for chapter in parser.chapters:
            entity, _ = Chapter.objects.update_or_create(
                ordinal=chapter['ordinal'],
                defaults={
                    'name': chapter['name'],
                    'section': section_entities[chapter['section_ordinal']]
                }
            )
            chapter_entities[chapter['ordinal']] = entity

        for clause in parser.clauses:
            chapter_entity = None
            if clause['chapter_ordinal']:
                chapter_entity = chapter_entities[clause['chapter_ordinal']]

            entity, _ = Clause.objects.update_or_create(
                number=clause['number'],
                defaults={
                    'name': clause['name'],
                    'clause_text': clause['clause_text'],
                    'chapter': chapter_entity
                }
            )

    def _fetch_takanon_wikitext(self, save_sources: bool) -> str:
        self.stdout.write('Fetching Takanon WikiCode')

        params = {
            'format': 'json',
            'action': 'query',
            'prop': 'revisions',
            'rvslots': 'main',
            'rvlimit': 1,
            'rvprop': 'content',
            'titles': 'תקנון_הכנסת'
        }
        url = 'https://he.wikisource.org/w/api.php?' + urllib.parse.urlencode(params)
            
        with urllib.request.urlopen(url) as response:
            self.stdout.write(f'Return code: {response.getcode()}')
            response_body = response.read()

            if save_sources:
                source_file = 'takanon.wiki'

                self.stdout.write(f"Saving WikiText into {source_file}")
                with open(source_file, 'wb') as f:
                    f.write(response_body)

            try:
                response_data = json.loads(response_body)
                return response_data['query']['pages']['316501']['revisions'][0]['slots']['main']['*']
            except (ValueError, KeyError) as e:
                self.stderr.write(f'Failed extracting WikiText from response: {repr(e)}')
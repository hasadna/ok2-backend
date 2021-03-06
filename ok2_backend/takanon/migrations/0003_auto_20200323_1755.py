# Generated by Django 2.2.7 on 2020-03-23 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('takanon', '0002_auto_20200217_1658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clause',
            name='clause_text',
        ),
        migrations.AddField(
            model_name='clause',
            name='latest_version',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.CreateModel(
            name='ClauseVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=30)),
                ('version_text', models.TextField()),
                ('clause', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='takanon.Clause')),
            ],
            options={
                'unique_together': {('clause', 'version')},
            },
        ),
    ]

# ok2-backend

This is the backend of Open Knesset v2.0 repository.
You can read more about the general idea in this document [כנסת פתוחה הדור הבא](https://github.com/hasadna/ok2-frontend/blob/master/about.pdf)

Also in the [frontend repo](https://github.com/hasadna/ok2-frontend)

### instalition
1. Make sure you installed python and add it to your PATH
1. Clone/Fork repo
1. Run in the ok2-backend folder:
- ````pip install -r requirements.txt```` (only once after pull)
- ````manage.py migrate```` to install database (only once after pull)
- ````manage.py runserver```` (to run localhost 8000 as)

###
- create super user: ```` python manage.py createsuperuser --email admin@example.com --username admin ````
![OK2](https://raw.githubusercontent.com/hasadna/ok2-frontend/master/assets/images/ok.png)

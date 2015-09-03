=====
django-simple-contacts
=====

django-simple-contacts is a Django app for making and managing simple set of contacts.

WARNING!!!
-----------
This app tested only with django 1.6

Quick start
-----------
1. You can install django-simple-contacts through pip::

      pip install django-simple-contacts

   or check out last version from github: https://github.com/renkse/django-simple-contacts.git

2. Add "contacts", flatpages and sites to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'contacts',
      )

3. Run `python manage.py syncdb` to create the contacts table.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create contacts (you'll need the Admin app enabled).

Requirements
------------
django==1.6, django-devtools

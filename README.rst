=====
Actions
=====

A simple Django app template tag for tagging actions.

Quick start
-----------

1. Add "actions" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'actions',
      )

2. Include the actions URLconf in your project urls.py like this::

      url(r'^actions/', include('actions.urls')),

3. Run `python manage.py syncdb` to create the actions models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a action (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/actions/ to participate in the action.
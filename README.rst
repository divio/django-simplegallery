django-simplegallery
====================

simple gallery

dependecies
-----------

* django-filer
* classy js: https://github.com/FinalAngel/classy-frontend-framework
* jquery
* jquery.cycle


Installation
------------

* `pip install django-simplegallery`
* follow the setup instructions for django-filer
* add `simplegallery` to INSTALLED_APPS and run syncdb or south migrate
* make sure `simplegallery/media` is accessible at your MEDIA_URL

* These external js dependencies also need to be made accessable at these
default locations:
  * `{{ MEDIA_URL }}js/libs/jquery-1.4.4.js`
  * `{{ MEDIA_URL }}js/libs/classy-1.3.js`
  * `{{ MEDIA_URL }}js/plugins/jquery.cycle-2.97.js`

You can change the locations of these files by overriding the templates.



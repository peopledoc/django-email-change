
=============
Configuration
=============

This section contains information about how to configure your Django projects
to use *django-email-change* and also contains a quick reference of the available
*settings* that can be used in order to customize the functionality of this
application.


Configuring your project
========================

In the Django project's ``settings`` module, add ``email_change`` to the
``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        ...
        'email_change',
    )


Update the project's URLs
=========================

*django-email-change* requires that you update your project's URL patterns by
adding the application's own URL set. In your project's ``urls`` module
add the following patterns::

    urlpatterns = patterns('',
        ...
        # URLs for django-email-change
        url('accounts/', include('email_change.urls')),
        ...
    )


Reference of the application settings
=====================================

The following settings can be specified in the Django project's ``settings``
module to customize the functionality of *django-email-change*.

``EMAIL_CHANGE_VERIFICATION_DAYS``
    How many days to keep the email request in the database.


Synchronize the project database
================================

Finally, synchronize the project's database using the following command::

    python manage.py syncdb


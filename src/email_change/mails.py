# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse_lazy as reverse
from django.contrib.auth import get_user_model

from mail_factory import factory
import uuid
from postbox.core.mails import BaseMailHeader, BaseMailForm

from email_change.models import EmailChangeRequest


class EmailChangeRequestMail(BaseMailHeader):
    template_name = 'email_change_request'
    params = ['email_request', 'activation_url']


def activation_url():
    return '%s%s' % (
        settings.SITE_URL, reverse('registration_activate',
                                   args=[str(uuid.uuid4()).replace('-', '')]))


class EmailChangeRequestForm(BaseMailForm):
    """Here, there is no inputs, all data is provided by get_context_data()."""
    def __init__(self, *args, **kwargs):
        if 'mail_class' in kwargs:
            self.mail_class = kwargs.pop('mail_class')
        forms.Form.__init__(self, *args, **kwargs)

    def get_context_data(self):
        User = get_user_model()
        user = User(username=u'johndoe',
                    first_name=u'John',
                    last_name=u'Doe',
                    title=u'Mr')
        email_request = EmailChangeRequest(user=user, email=user.email)
        url = activation_url()
        return {'email_request': email_request,
                'activation_url': url}


factory.register(EmailChangeRequestMail, EmailChangeRequestForm)

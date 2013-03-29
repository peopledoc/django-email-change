# -*- coding: utf-8 -*-
from mail_factory import factory
from postbox.core.mails import BaseMailHeader, BaseMailForm

from django.conf import settings
from django.core.urlresolvers import reverse_lazy as reverse
import uuid


class EmailChangeRequestMail(BaseMailHeader):
    template_name = 'email_change_request'
    params = ['email_request', 'activation_url']


def activation_url():
    return '%s%s' % (
        settings.SITE_URL, reverse('registration_activate',
                                   args=[str(uuid.uuid4()).replace('-', '')]))


class EmailChangeRequestForm(BaseMailForm):
    class Meta:
        mail_class = EmailChangeRequestMail
        initial = {'email_request': 1,
                   'activation_url': activation_url}

factory.register(EmailChangeRequestMail, EmailChangeRequestForm)

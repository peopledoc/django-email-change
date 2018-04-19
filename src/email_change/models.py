# -*- coding: utf-8 -*-
#
#  This file is part of django-email-change.
#
#  django-email-change adds support for email address change and confirmation.
#
#  Development Web Site:
#    - http://www.codetrax.org/projects/django-email-change
#  Public Source Code Repository:
#    - https://source.codetrax.org/hgroot/django-email-change
#
#  Copyright 2010 George Notaras <gnot [at] g-loaded.eu>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.core.urlresolvers import reverse_lazy as reverse

from django.conf import settings


EMAIL_CHANGE_VERIFICATION_DAYS = getattr(settings, 'EMAIL_CHANGE_VERIFICATION_DAYS', 7)


class EmailChangeRequest(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,  related_name='%(class)s_user')
    verification_key = models.CharField(max_length=40)
    email = models.EmailField(max_length=75)  # Contains the new email address
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'email change request'
        verbose_name_plural = 'email change requests'

    def save(self, *args, **kwargs):
        if not self.verification_key:
            self.verification_key = generate_key(self.user, self.email)
        return super(EmailChangeRequest, self).save(*args, **kwargs)

    def __unicode__(self):
        return '(%s) %s --> %s' % (self.user.username, self.user.email,
                                   self.email)

    def is_creation_request(self):
        return self.email == self.user.email

    def has_expired(self):
        dt = timedelta(days=EMAIL_CHANGE_VERIFICATION_DAYS)
        expiration_date = self.date_created + dt
        return expiration_date <= now() and not self.is_creation_request()

    def get_mail_context(self):
        context_params = {
            'email_request': self,
            'activation_url': "%s%s?code=%s" % (
                settings.SITE_URL,
                reverse('email_verify', args=[self.verification_key]),
                self.verification_key)
        }
        return context_params

    def send(self, template_dir='email_change_request'):
        """
        Send a mix html/txt email_change_request email
        """
        context_params = self.get_mail_context()
        factory.mail(
            template_dir,
            emails=[self.email],
            context=context_params,
            from_email=settings.DEFAULT_FROM_EMAIL)

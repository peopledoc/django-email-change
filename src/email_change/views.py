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

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from email_change.models import EmailChangeRequest
from email_change.forms import EmailChangeForm


@login_required
def email_change_view(request, extra_context={},
                      success_url='email_verification_sent',
                      template_name='email_change/email_change_form.html',
                      email_message_template_name='email_change_request',
                      form_class=EmailChangeForm):
    """Allow a user to change the email address associated with the
    user account.

    """
    if request.method == 'POST':
        form = form_class(username=request.user.username,
                          data=request.POST,
                          files=request.FILES)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            # First clean all email change requests made by this user
            # Except subscription email validation
            qs = EmailChangeRequest.objects.filter(user=request.user) \
                                           .exclude(email=request.user.email)
            qs.delete()

            # Create an email change request
            email_request = EmailChangeRequest.objects.create(
                user=request.user,
                email=email
            )

            email_request.send(email_message_template_name)

            return redirect(success_url)

    else:
        form = form_class(username=request.user.username)

    context = RequestContext(request, extra_context)
    context['form'] = form

    return render_to_response(template_name, context_instance=context)


def email_verify_view(request, verification_key, extra_context={},
                      success_url='email_change_complete',
                      template_name='email_change/email_verify.html'):
    """
    """
    context = RequestContext(request, extra_context)
    try:
        ecr = EmailChangeRequest.objects.get(verification_key=verification_key)
    except EmailChangeRequest.DoesNotExist:
        # Return failure response
        return render_to_response(template_name, context_instance=context)
    else:
        # Check if the email change request has expired
        if ecr.has_expired():
            ecr.delete()
            # Return failure response
            return render_to_response(template_name, context_instance=context)

        # Success. Replace the user's email with the new email
        ecr.user.email = ecr.email
        ecr.user.save()

        # Delete the email change request
        ecr.delete()

        # Redirect to success URL
        return redirect(success_url)


@login_required
def email_verification_resend(request, pk):
    email_request = get_object_or_404(
        EmailChangeRequest.objects.filter(user=request.user), pk=pk)
    email_request.send()
    messages.success(request, _('Email change request has been resent.'))
    return redirect('vault:index')


@login_required
def email_verification_cancel(request, pk):
    email_request = get_object_or_404(
        EmailChangeRequest.objects.filter(user=request.user), pk=pk)
    email_request.delete()
    messages.success(request, _('Email change request has been cancelled.'))
    return redirect('vault:index')

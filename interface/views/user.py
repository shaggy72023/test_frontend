import json

from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.utils.decorators import method_decorator

from blog import settings
from decorators.custom_decorators import active_session_required
from interface.mixins import BackendMixin

from utils.api_clients.backend import FormValidationFailsApiClientError, WrongCredentialsAPIClientError, \
    WrongAuthorizeHeadersAPIClientError, UserDoesNotExistClientAPIError, WrongActivationCodeApiClientError


class SighUp(BackendMixin, View):

    def get(self, request):
        return render(request, 'interface/user/signup.html')

    def post(self, request):
        try:
            form_data = request.POST.dict()
            form_data['email_activation_url'] = settings.MAIN_WEBSITE_URL + reverse('interface:activate')
            response = self.backend.user.post(data=json.dumps(form_data))

        except FormValidationFailsApiClientError as e:
            messages.error(request, e.message)
            return render(request, 'interface/user/signup.html')

        request.session['access_token'] = response['access_token']
        request.session['user_id'] = response['user_id']
        return redirect('interface:account')


class Login(BackendMixin, View):

    def get(self, request):
        return render(request, 'interface/user/login.html')

    def post(self, request):

        try:
            response = self.backend.user.login_user(data=json.dumps(request.POST))

        except WrongCredentialsAPIClientError:
            messages.error(request, 'Wrong username or password')
            return render(request, 'interface/user/login.html')

        request.session['access_token'] = response['access_token']
        request.session['user_id'] = response['user_id']
        return redirect('interface:account')


class Account(BackendMixin, View):

    @method_decorator(active_session_required)
    def get(self, request):
        user_id = request.session['user_id']
        headers = self.generate_secure_headers(request)
        try:
            user = self.backend.user.get(user_id, headers=headers)

        except WrongAuthorizeHeadersAPIClientError:
            request.session.flush()
            return HttpResponseForbidden('403 Forbidden')

        except UserDoesNotExistClientAPIError:
            return HttpResponseForbidden('403 Forbidden')

        return render(request, 'interface/user/account.html', {'user': user})


class ActivateUser(BackendMixin, View):
    def get(self, request):
        mail_data = request.GET.dict()
        mail_data['email_activation_url'] = settings.MAIN_WEBSITE_URL + reverse('interface:activate')

        try:
            self.backend.user.put(data=json.dumps(mail_data))
            return render(request, 'interface/user/activated.html')

        except WrongActivationCodeApiClientError:
            return render(request, 'interface/user/not_activated.html')


class Logout(View):
    def get(self, request):
        request.session.flush()
        return redirect('interface:login')


import json

from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.utils.decorators import method_decorator

from decorators.custom_decorators import active_session_required
from interface.mixins import BackendMixin

from utils.api_clients.backend import UsernameExistsAPIClientError, WrongCredentialsAPIClientError, \
    WrongAuthorizeHeadersAPIClientError, UserDoesNotExistClientAPIError


class SighUp(BackendMixin, View):

    def get(self, request):
        return render(request, 'interface/user/signup.html')

    def post(self, request):
        try:
            response = self.backend.user.post(data=json.dumps(request.POST))

        except UsernameExistsAPIClientError:
            messages.error(request, 'Oops, username already exists')
            return render(request, 'interface/user/signup.html')

        request.session['access_token'] = response['access_token']
        request.session['user_id'] = response['user_id']
        return redirect('interface:account', response['user_id'])


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
        return redirect('interface:account', response['user_id'])


class Account(BackendMixin, View):

    @method_decorator(active_session_required)
    def get(self, request, user_id):
        headers = self.generate_secure_headers(request)
        try:
            user = self.backend.user.get(user_id, headers=headers)

        except (WrongAuthorizeHeadersAPIClientError, UserDoesNotExistClientAPIError):
            return HttpResponseForbidden('403 Forbidden')

        return render(request, 'interface/user/account.html', {'user': user})


class LogOut(View):
    def get(self, request):
        request.session.flush()
        return redirect('interface:login')


from django.shortcuts import redirect
from django.views.generic import View
from django.utils.decorators import method_decorator

from interface.mixins import BackendMixin
from decorators.custom_decorators import active_session_required

import json


class Comment(BackendMixin, View):

    @method_decorator(active_session_required)
    def post(self, request):
        post_data = request.POST.dict()
        post_data['user_id'] = request.session['user_id']
        headers = self.generate_secure_headers(request)
        self.backend.comment.post(data=json.dumps(post_data), headers=headers)
        return redirect('interface:post:view', post_id=post_data['post'])


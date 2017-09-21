from django.views.generic import ListView, DetailView

from interface.mixins import BackendMixin, PostMixin


class List(BackendMixin, ListView):

    context_object_name = 'posts'
    template_name = 'interface/post/list.html'

    def get_queryset(self):
        return self.backend.post.all()


class View(BackendMixin, PostMixin, DetailView):

    context_object_name = 'post'
    template_name = 'interface/post/view.html'

    def get_object(self, queryset=None):
        return self.post

    def get_context_data(self, **kwargs):
        context = super(View, self).get_context_data(**kwargs)
        context['comments'] = self.post.comments
        context['user_authenticated'] = 'access_token' in self.request.session
        return context

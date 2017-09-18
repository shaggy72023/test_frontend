from django.conf.urls import patterns, include, url

from .views import post, user


urlpatterns = patterns('',
    url('^post', include(patterns('',
        url(r'^$', post.List.as_view(), name='list'),
        url(r'^/(?P<post_id>\d+)$', post.View.as_view(), name='view'),
    ), namespace='post')),
    url('^signup', user.SighUp.as_view(), name='signup'),
    url('^login', user.Login.as_view(), name='login'),
    url('^logout', user.LogOut.as_view(), name='logout'),
    url('^account/(?P<user_id>\d+)$', user.Account.as_view(), name='account')
)

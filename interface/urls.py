from django.conf.urls import patterns, include, url

from .views import post, user, comment


urlpatterns = patterns('',
    url('^post', include(patterns('',
        url(r'^$', post.List.as_view(), name='list'),
        url(r'^/(?P<post_id>\d+)$', post.View.as_view(), name='view'),
    ), namespace='post')),
    url('^signup$', user.SighUp.as_view(), name='signup'),
    url('^login$', user.Login.as_view(), name='login'),
    url('^logout$', user.Logout.as_view(), name='logout'),
    url('^activate$', user.ActivateUser.as_view(), name='activate'),
    url('^account$', user.Account.as_view(), name='account'),
    url('^comment$', comment.Comment.as_view(), name='comment')
)

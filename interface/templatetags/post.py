import hashlib
import urllib

from django import template

register = template.Library()


@register.filter
def gravatar_url(email, size=40):
    default = "https://www.drupal.org/files/issues/default-avatar.png"
    return "https://www.gravatar.com/avatar/{0}?{1}".format(
        hashlib.md5(email.lower()).hexdigest(),
        urllib.urlencode({'d': default, 's': str(size)})
    )
from django.conf import settings

from utils.api_clients.backend import BackendAPIClient
import datetime
import hashlib
import hmac


class BackendMixin(object):

    @property
    def backend(self):
        return BackendAPIClient(settings.BACKEND_API_URL)

    def generate_secure_headers(self, request):
        access_token = request.session.get('access_token')
        user_id = request.session.get('user_id')

        if access_token is None or user_id is None:
            return {}

        access_token = str(access_token)
        t = datetime.datetime.utcnow()
        datestamp = t.strftime('%Y%m%dT%H%M%SZ')
        string_to_sign = datestamp + str(user_id)
        signature = hmac.new(access_token, string_to_sign.encode('utf-8'), hashlib.sha256).digest()
        signature = signature.encode('base-64').strip()
        return {'date': datestamp, 'Authorization': signature}

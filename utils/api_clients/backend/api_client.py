import tortilla

from .exceptions import api_exception_register, APIClientError


class Resource(object):

    def __init__(self, resource):
        self._resource = resource

    @property
    def resource(self):
        return self._resource

    def all(self, **options):
        return self.process_result(self.resource.get(**options))

    def get(self, id, **options):
        return self.process_result(self.resource.get(id, **options))

    def post(self, **options):
        return self.process_result(self.resource.post(**options))

    def put(self, **options):
        return self.process_result(self.resource.put(**options))

    def process_result(self, result):

        if not result['success']:
            raise api_exception_register.get(result['error']['code'], APIClientError)(result['error']['message'])

        return result['result']


class Post(Resource):

    @property
    def resource(self):
        return self._resource.posts


class User(Resource):

    @property
    def resource(self):
        return self._resource.users

    def login_user(self, **options):
        return self.process_result(self.resource.login.post(**options))


class BackendAPIClient(object):

    def __init__(self, api_url):

        self.api_url = api_url
        self.resource = tortilla.wrap(api_url)

        self.post = Post(self.resource)
        self.user = User(self.resource)

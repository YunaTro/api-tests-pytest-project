class BaseApiClient:
    def __init__(self, session, base_url, timeout=(10, 25)):
        self.session = session
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def request(self, method, path, **kwargs):
        url = self.build_url(path)
        kwargs.setdefault("timeout", self.timeout)
        return self.session.request(method, url, **kwargs)

    def build_url(self, path):
        return f"{self.base_url}/{path.lstrip('/')}"
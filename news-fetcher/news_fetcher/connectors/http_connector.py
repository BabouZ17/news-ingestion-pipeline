from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class HTTPConnector:
    def __init__(self):
        self.session = self._build_session()

    @staticmethod
    def _build_session() -> Session:
        retries = Retry(
            total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
        )

        session = Session()
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def get(self, *args, **kwargs) -> Response:
        return self.session.get(*args, **kwargs)

    def post(self, *args, **kwargs) -> Response:
        return self.session.post(*args, **kwargs)

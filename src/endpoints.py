from urllib.parse import urljoin


class Endpoints:
    def __init__(self, host: str):
        self._host = host

    def host_append(self, v: str):
        url = urljoin(self._host, v)
        return url

    @property
    def add_to_meeting(self):
        return self.host_append("/hooks/yes_meeting")

    @property
    def not_meeting(self):
        return self.host_append("/hooks/no_meeting")

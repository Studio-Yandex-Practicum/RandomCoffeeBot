from urllib.parse import urljoin


class Endpoints:
    def __init__(self, host: str):
        self._host = host

    def host_append(self, v: str):
        url = urljoin(self._host, v)
        return url

    @property
    def add_to_meeting(self):
        return self.host_append("/hooks/set_waiting_meeting_status")

    @property
    def not_meeting(self):
        return self.host_append("/hooks/not_meeting")

    @property
    def answer_yes(self):
        return self.host_append("/hooks/match_review_answer_yes")

    @property
    def answer_no(self):
        return self.host_append("/hooks/match_review_answer_no")

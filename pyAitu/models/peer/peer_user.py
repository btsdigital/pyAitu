from .peer import Peer


class PeerUser(Peer):
    def __init__(self, json_object):
        super().__init__(json_object)
        self._first_name = json_object['firstName']
        self._last_name = json_object['lastName']
        self._username = json_object['username'] if 'username' in json_object else None

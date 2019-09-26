class Peer:
    def __init__(self, json_object):
        self.id = json_object["id"]
        self.type = json_object["type"]

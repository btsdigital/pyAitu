class Audio:
    def __init__(self, json_object):
        self.type = json_object.get("type")
        self.fileId = json_object.get("fileId")
        self.mimeType = json_object.get("mimeType")
        self.name = json_object.get("name")
        self.size = json_object.get("size")

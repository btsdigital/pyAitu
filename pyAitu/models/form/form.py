class Form:
    def __init__(self, _id: str, content, header):
        self.id = _id
        self.header = header
        self.content = content

    def make_form(self):
        return {
            "form": {
                "id": self.id,
                "header": self.header.__dict__,
                "content": [self.content.__dict__]
            }
        }

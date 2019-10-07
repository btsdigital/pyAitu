class Form:
    def __init__(self, _id: str, content, header):
        self.id = _id
        self.header = header
        self.content = content

    def make_form(self):
        result = []
        if isinstance(self.content, list):
            for el in self.content:
                result.append(remove_none(el.__dict__))
        else:
            result.append(self.content.__dict__)
        return {
            "form": {
                "id": self.id,
                "header": self.header.__dict__,
                "content": result
            }
        }


def remove_none(command: dict):
    return {k: v for k, v in command.items() if v is not None}

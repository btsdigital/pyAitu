from .options import Options


class Form:
    def __init__(self, _id: str, content, header, options: Options = None):
        self.id = _id
        self.header = header
        self.content = content
        self.options = options

    def make_form(self):
        result = []

        # Above three lines return self.options without None in value
        dict_options = dict
        if self.options is not None:
            dict_options = {k: v for k, v in self.options.__dict__.items() if v is not None}

        if isinstance(self.content, list):
            for el in self.content:
                result.append(remove_none(el.__dict__))
        else:
            result.append(self.content.__dict__)
        return {
            "form": {
                "id": self.id,
                "header": self.header.__dict__,
                "content": result,
                "options": dict_options if self.options is not None else {}
            }
        }


def remove_none(command: dict):
    return {k: v for k, v in command.items() if v is not None}

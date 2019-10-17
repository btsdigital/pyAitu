class WebhookInfo:
    def __init__(self, json_object):
        self.url = json_object.get("url")

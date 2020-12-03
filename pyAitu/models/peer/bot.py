class Bot:
    def __init__(self, json_object):
        self.id = json_object['botId']
        self.name = json_object['name']
        self.username = json_object['username']

    def __str__(self):
        return "{%s %s %s}" % (self.id, self.name, self.username)

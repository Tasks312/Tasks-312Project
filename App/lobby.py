import json

class Lobby:
    MAX = 2

    def __init__(self, id: int, title: str, desc: str):
        self.id = id
        self.title = title
        self.desc = desc

        self.users = []

    def as_obj(self):
        return {
            "id": self.id,
            "lobby_title": self.title,
            "lobby_description": self.desc,
            "users": self.users
        }

    def as_json(self):
        return json.dumps(self.as_obj())


def from_obj(obj):
    out = Lobby(obj["id"], obj["lobby_title"], obj["lobby_description"])
    out.users = obj["users"]

    return out

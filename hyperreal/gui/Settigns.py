import json

settings_file = "settings.json"


class Settings:

    def __init__(self):
        self.last_crawl = "1990-01-01"

        try:
            with open(settings_file, "r") as f:
                loaded = json.load(f)
                self.last_crawl = loaded["last_crawl"]
        except FileNotFoundError as e:
            print(e)

    def safe(self):
        new_json = {"last_crawl": self.last_crawl}
        with open(settings_file, "w") as f:
            f.write(json.dumps(new_json))
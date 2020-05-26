import json
from datetime import date
import os
import errno

settings_file = "settings.json"


class Settings:

    def __init__(self):
        self.data_folder = "data"
        self.temp_folder = "temp"

        self._ensure_dir_exists(self.data_folder)
        self._ensure_dir_exists(self.temp_folder)

        self.last_crawl = date(1990, 1, 1)
        try:
            with open(settings_file, "r") as f:
                loaded = json.load(f)
                self.last_crawl = date.fromisoformat(loaded["last_crawl"])
        except FileNotFoundError as e:
            print(e)

    def save(self):
        new_json = {"last_crawl": self.last_crawl}
        with open(settings_file, "w") as f:
            f.write(json.dumps(new_json))

    def _ensure_dir_exists(self, path):
        if not os.path.exists(path):
            try:
                os.mkdir(self.data_folder)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

import json
import os

CONFIG_FILE = "config/settings.json"


class ConfigManager:

    @staticmethod
    def load():

        if not os.path.exists(CONFIG_FILE):
            return {
                "master_file": "",
                "visualizer_folder": ""
            }

        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def save(config):

        os.makedirs("config", exist_ok=True)

        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            json.dump(config, file, indent=4)
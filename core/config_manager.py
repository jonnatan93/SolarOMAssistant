import json
from pathlib import Path


class ConfigManager:

    CONFIG_FILE = Path("settings.json")

    DEFAULT_CONFIG = {
        "master_file": "",
        "visualizer_folder": ""
    }

    @classmethod
    def load(cls):

        if not cls.CONFIG_FILE.exists():

            cls.save(cls.DEFAULT_CONFIG)

            return cls.DEFAULT_CONFIG.copy()

        try:

            with open(
                cls.CONFIG_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            config = cls.DEFAULT_CONFIG.copy()

            config.update(data)

            return config

        except Exception:

            return cls.DEFAULT_CONFIG.copy()

    @classmethod
    def save(cls, config):

        with open(
            cls.CONFIG_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                config,
                f,
                indent=4,
                ensure_ascii=False
            )
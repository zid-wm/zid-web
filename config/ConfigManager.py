import configparser
import os


class ConfigManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(f'config/{os.environ.get("CONFIG_ENV")}_config.ini')

    def database(self):
        if 'database' in self.config:
            return self.config['database']
        else:
            return []

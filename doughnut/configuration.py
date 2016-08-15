import os
import ujson
from jsonschema import validate
from doughnut import settings

class Configuration:
    def __init__(self, source):
        self.source = source

    def read(self):
        with open(settings.SCHEMA_FILE, 'rb') as schema_file:
            schema = ujson.loads(schema_file.read())
            config = ujson.loads(self.source.read(settings.CONFIG_FILE_NAME))
            validate(config, schema)
            return config

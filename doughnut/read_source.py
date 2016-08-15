import os
import pathlib
import zipfile
from doughnut import settings
from doughnut.exceptions import InvalidSource

class ReadSource:
    def __init__(self, source_path):
        self.source_path = source_path

        if os.path.isdir(source_path):
            self.is_zip = False
        elif zipfile.is_zipfile(source_path):
            self.is_zip = True
            self.basepath = self.__get_base()
        else:
            raise InvalidSource("Supplied source is not a valid zip or not a directory")

    def __get_base(self):
        with zipfile.ZipFile(self.source_path) as source_zip:
            for f in source_zip.namelist():
                if os.path.basename(f) == settings.CONFIG_FILE_NAME:
                    p = str(pathlib.Path(f).parent)

                    if(p == '.'):
                        p = ''

                    return p

        raise InvalidSource("Supplied source dosen't contain %s file" % settings.CONFIG_FILE_NAME)

    def sanitize(self, filename):
        return os.path.basename(filename)

    def read(self, filename):
        filename = self.sanitize(filename)
        if self.is_zip:
            with zipfile.ZipFile(self.source_path) as source_zip:
                with source_zip.open(os.path.join(self.basepath, filename)) as source:
                    return source.read().decode('UTF-8')
        else:
            with open(os.path.join(self.source_path, filename), 'r') as source:
                    return source.read()

    def readBytes(self, filename, size=''):
        filename = self.sanitize(filename)
        if self.is_zip:
            with zipfile.ZipFile(self.source_path) as source_zip:
                with source_zip.open(os.path.join(self.basepath, filename)) as source:
                    if size == '':
                        return source.read()
                    else:
                        return source.read(size)
        else:
            with open(os.path.join(self.source_path, filename), 'rb') as source:
                if size == '':
                    return source.read()
                else:
                    return source.read(size)

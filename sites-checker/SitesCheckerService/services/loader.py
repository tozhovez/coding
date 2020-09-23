import requests

class Loader:
    def __init__(self,
                 url: str,
                 path: str,
                 permissions: str):
        self.url = url
        self.permissions = permissions
        self.path = path

        self._file = None

    def __enter__(self):
        self._file = open(self.path, self.permissions)

        if 'w' in self.permissions:
            self._file.truncate(0)
        return self

    def __exit__(self, type, value, traceback):
        self._file.close()

    def load_data(self):
        rawtext = requests.get(self.url).text
        self._file.write(rawtext)

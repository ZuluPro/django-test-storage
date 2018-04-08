from django.core.files.storage import Storage
from django.core.files import File
from django.utils import timezone


class handled_files(dict):
    """
    Dict for gather information about fake storage and clean between tests.
    You should use the constant instance ``HANDLED_FILES`` and clean it
    before tests.
    """
    def __init__(self):
        super(handled_files, self).__init__()
        self.clean()

    def clean(self):
        self['written_files'] = []
        self['deleted_files'] = []

HANDLED_FILES = handled_files()


class FakeStorage(Storage):
    name = 'FakeStorage'

    def exists(self, name):
        return name in [i for i, j in HANDLED_FILES['written_files']]

    def get_available_name(self, name, max_length=None):
        return name[:max_length]

    def get_valid_name(self, name):
        return name

    def listdir(self, path):
        return ([], [f[0] for f in HANDLED_FILES['written_files']])

    def accessed_time(self, name):
        return timezone.now()
    created_time = modified_time = accessed_time

    def _open(self, name, mode='rb'):
        file_ = [f[1] for f in HANDLED_FILES['written_files']
                 if f[0] == name][0]
        file_.seek(0)
        return file_

    def _save(self, name, content):
        HANDLED_FILES['written_files'].append((name, File(content)))
        return name

    def delete(self, name):
        HANDLED_FILES['deleted_files'].append(name)

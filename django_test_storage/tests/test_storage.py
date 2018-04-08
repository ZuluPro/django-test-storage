from io import StringIO
from django.test import TestCase
from django.utils import timezone
from django_test_storage import FakeStorage, HANDLED_FILES


class FakeStorageTest(TestCase):
    def setUp(self):
        self.storage = FakeStorage()

    def tearDown(self):
        HANDLED_FILES.clean()

    def test_exists(self):
        self.storage._save('foo', StringIO('bar'))
        exists = self.storage.exists('foo')
        self.assertTrue(exists)

    def test_not_exists(self):
        exists = self.storage.exists('foo')
        self.assertFalse(exists)

    def test_get_available_name(self):
        name = 'foo'
        available_name = self.storage.get_available_name(name)
        self.assertEqual(name, available_name)

    def test_get_valid_name(self):
        name = 'foo'
        valid_name = self.storage.get_valid_name(name)
        self.assertEqual(name, valid_name)

    def test_listdir(self):
        # Empty
        files = self.storage.listdir('')
        self.assertEqual(files, ([], []))
        # 1 file
        self.storage._save('foo', StringIO('bar'))
        dirs, files = self.storage.listdir('')
        self.assertEqual(len(files), 1)

    def test_accessed_time(self):
        date = timezone.now().date()
        file_date = self.storage.accessed_time('foo').date()
        self.assertEqual(date, file_date)

    def test_created_time(self):
        date = timezone.now().date()
        file_date = self.storage.created_time('foo').date()
        self.assertEqual(date, file_date)

    def test_modified_time(self):
        date = timezone.now().date()
        file_date = self.storage.modified_time('foo').date()
        self.assertEqual(date, file_date)

    def test_open(self):
        self.storage._save('foo', StringIO('bar'))
        file_ = self.storage._open('foo')
        self.assertEqual(file_.read(), 'bar')

    def test_save(self):
        self.storage._save('foo', StringIO('bar'))
        file_ = self.storage._open('foo')
        self.assertEqual(file_.read(), 'bar')

    def test_delete(self):
        self.storage._save('foo', StringIO('bar'))
        file_ = self.storage.delete('foo')

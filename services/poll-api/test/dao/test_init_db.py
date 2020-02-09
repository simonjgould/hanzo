from unittest import TestCase
from unittest.mock import patch

from dao.db import init_db


class TestDbInitDb(TestCase):
    @patch("dao.db.get_settings")
    @patch('dao.db.PostgresqlDatabase')
    def test_given_settings_when_initdb_called_then_postgres_db_created(self, mock_pg_db, mock_settings):
        mock_db_instance = mock_pg_db.return_value
        mock_settings.return_value = {
            'NAME': "test_name",
            'USER': "test_user",
            'PASSWORD': "test_password",
            'HOST': "test_host",
            'PORT': "test_post"
        }
        rv = init_db()
        self.assertEqual(mock_db_instance, rv)
        mock_pg_db.assert_called_once_with("test_name", user="test_user", password="test_password",
                                           host="test_host", port="test_post")

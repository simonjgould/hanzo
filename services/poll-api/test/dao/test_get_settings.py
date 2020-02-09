from unittest import TestCase
from unittest.mock import patch

from dao import settings


class TestGetSettings(TestCase):
    def test_given_empty_environment_when_get_settings_called_then_key_error_raised(self):
        with self.assertRaises(KeyError) as key_error:
            settings.get_settings()

        self.assertEqual("KeyError('DB_HOST')", repr(key_error.exception))

    @patch.dict(settings.os.environ, {
        "DB_HOST": "test_host",
        "DB_PORT": "test_port",
        "DB_NAME": "test_name",
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password"
    })
    def test_given_environment_set_up_when_get_settings_called_then_correct_settings_returned(self):
        self.assertDictEqual({
            'HOST': 'test_host',
            'NAME': 'test_name',
            'PASSWORD': 'test_password',
            'PORT': 'test_port',
            'USER': 'test_user'
        }, settings.get_settings())

from unittest import TestCase
from unittest.mock import Mock, patch

from dao import models


class TestQuestion(TestCase):
    @patch.dict(models.os.environ, {
        "VERSION_ID": "test"
    })
    def test_given_db_when_set_db_called_then_meta_database_set_and_db_table_created(self):
        mock_db = Mock()
        mock_db.table_exists.return_value = False

        models.Question.set_db(mock_db)

        mock_db.table_exists.assert_called_once_with("test_question")
        mock_db.create_tables.assert_called_once_with([models.Question])

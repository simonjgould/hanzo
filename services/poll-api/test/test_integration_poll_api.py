from unittest import TestCase
from unittest.mock import patch
import datetime
import json

from peewee import SqliteDatabase

from dao import settings
from dao.models import Question

import poll_api

models = [Question]

test_db = SqliteDatabase(':memory:')


class PollApiIntTest(TestCase):
    def setUp(self):
        with patch.dict(settings.os.environ, {
            "DB_HOST": "test_host",
            "DB_PORT": "test_port",
            "DB_NAME": "test_name",
            "DB_USER": "test_user",
            "DB_PASSWORD": "test_password",
            "VERSION_ID": "test"
        }):
            with patch('dao.db.PostgresqlDatabase') as mock_pg_db:
                mock_pg_db.return_value = test_db
                app = poll_api.create_app()

        mock_pg_db.assert_called_once_with("test_name", user="test_user", password="test_password",
                                           host="test_host", port="test_port")
        print(str(test_db.get_tables()))
        app.config['TESTING'] = True
        self.client = app.test_client()

    def tearDown(self):
        test_db.drop_tables(models)
        test_db.close()

    def test_given_initial_set_up_when_get_questions_then_empty_json_array_response(self):
        rv = self.client.get('/polls/questions/')
        self.assertEqual('[]', rv.data.decode())

    def test_given_test_data_set_up_when_get_questions_then_empty_json_array_response(self):
        test_date = datetime.datetime.now().date()
        question = Question(question_text="test question", pub_date=test_date)
        question.save()

        rv = self.client.get('/polls/questions/')
        self.assertEqual(json.dumps([
            {
                "question_text": "test question",
                "id": 1,
                "pub_date": str(test_date)
            }
        ]), rv.data.decode())

    def test_given_initial_set_up_when_post_questions_then_database_updated(self):
        test_date = datetime.datetime.now().date()
        payload = {
            "question_text": "test question post",
            "pub_date": str(test_date)
        }
        rv = self.client.post('/polls/questions/', data=json.dumps(payload), content_type='application/json')
        self.assertDictEqual({
            "question_text": "test question post",
            "id": 1,
            "pub_date": str(test_date)
        }, json.loads(rv.data.decode()))
        questions = Question.select()
        for question in questions:
            self.assertDictEqual({
                "question_text": "test question post",
                "id": 1,
                "pub_date": str(test_date)
            }, {
                'question_text': question.question_text,
                'id': question.id,
                'pub_date': question.pub_date.strftime('%Y-%m-%d')
            })

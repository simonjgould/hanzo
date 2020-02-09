import os
import json
from datetime import datetime
from redis import Redis

from flask import Flask, request

from dao.db import init_db
from dao.models import Question


def create_app():
    app = Flask(__name__)

    redis = Redis(host=os.environ["REDIS_HOST"], port=int(os.environ["REDIS_PORT"]), db=0)
    Question.set_db(init_db())

    @app.route('/polls/questions/', methods=['GET', 'POST'])
    def questions():
        redis.incr("hits", amount=1)
        try:
            if request.method == 'POST':
                app.logger.debug("request:form {}".format(json.dumps(request.get_json())))
                question_text = request.json["question_text"]
                pub_date = datetime.strptime(request.json['pub_date'], '%Y-%m-%d')
                question = Question(question_text=question_text, pub_date=pub_date)
                question.save()
                resp = {'question_text': question.question_text, 'id': question.id,
                        'pub_date': question.pub_date.strftime('%Y-%m-%d')}
                return json.dumps(resp)
            if request.method == 'GET':
                questions = Question.select()
                questions_list = []
                for question in questions:
                    questions_list.append({'question_text': question.question_text, 'id': question.id,
                              'pub_date': question.pub_date.strftime('%Y-%m-%d')})
                return json.dumps(questions_list)
        except Exception as ex:
            app.logger.error("questions {}".format(repr(ex)))
            raise ex

    @app.route('/hits/', methods=['GET'])
    def hits():
        return json.dumps({'hits': int(redis.get('hits').decode('utf-8'))})

    return app

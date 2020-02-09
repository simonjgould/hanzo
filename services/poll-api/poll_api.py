import json
from datetime import datetime

from flask import Flask, request

from dao.db import init_db
from dao.models import Question


def create_app():
    app = Flask(__name__)

    Question.set_db(init_db())

    @app.route('/polls/questions/', methods=['GET', 'POST'])
    def questions():
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
                l = []
                for question in questions:
                    l.append({'question_text': question.question_text, 'id': question.id,
                              'pub_date': question.pub_date.strftime('%Y-%m-%d')})
                return json.dumps(l)
        except Exception as ex:
            app.logger.error("questions {}".format(repr(ex)))
            raise ex

    return app

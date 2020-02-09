import os
from peewee import Model, CharField, DateField


class Question(Model):
    question_text = CharField()
    pub_date = DateField()

    class Meta:
        table_name = None
        database = None

    @classmethod
    def set_db(cls, db):
        cls._meta.table_name = '{}_question'.format(os.environ["VERSION_ID"])
        cls._meta.database = db
        if db.table_exists(cls._meta.table_name) is False:
            db.create_tables([Question])

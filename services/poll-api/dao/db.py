from peewee import PostgresqlDatabase

from .settings import get_settings


def init_db():
    settings = get_settings()
    return PostgresqlDatabase(
        settings['NAME'], user=settings['USER'], password=settings['PASSWORD'],
        host=settings['HOST'], port=settings['PORT']
    )

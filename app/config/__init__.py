import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.join(os.path.join(os.path.dirname(__file__), '..'), '..'), '.env')
load_dotenv(dotenv_path=env_path, override=True)


class App:
    debug: bool = True if os.getenv('APP_DEBUG') == "True" else False
    port: int = int(os.getenv('APP_PORT'))
    host: str = os.getenv('APP_HOST')
    api_key: str = os.getenv('SECURE_API_KEY')
    sentry_dsn: str = os.getenv('SENTRY_DSN')
    init_sentry: str = os.getenv('INIT_SENTRY')
    init_db: str = os.getenv('INIT_DB')
    enable_gunicorn_logger = os.getenv('ENABLE_GUNICORN_LOGGER')
    root = os.path.dirname(os.path.abspath(__file__)).replace('config', '')
    temp_image_folder = os.path.join("{}{}{}".format('.', os.sep, "images/temp"))
    temp_folder = os.path.join(root, "{}{}".format(os.sep, os.getenv('TEMP_FOLDER')))
    models_folder = os.path.join(root, "{}{}".format(os.sep, "trained_models"))


class DB:
    driver: str = os.getenv('DB_CONNECTION')
    username: str = os.getenv('DB_USERNAME')
    password: str = os.getenv('DB_PASSWORD')
    hostname: str = os.getenv('DB_HOST')
    port: int = int(os.getenv('DB_PORT'))
    database: str = os.getenv('DB_DATABASE')

    @staticmethod
    def to_string():
        return DB.driver + '://' + DB.username + ':' + DB.password + '@' + \
               DB.hostname + ':' + str(DB.port) + '/' + DB.database


class Porichoy:
    url: str = os.getenv('PORICHOY_URL')
    api_key: str = os.getenv('PORICHOY_API_KEY')

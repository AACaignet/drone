
import os

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
#     os.environ.get('POSTGRES_USER', 'postgres'),
#     os.environ.get('POSTGRES_PASSWORD', 'postgres'),
#     os.environ.get('POSTGRES_SERVER', 'localhost'),
#     os.environ.get('POSTGRES_PORT', 5432),
#     os.environ.get('POSTGRES_DBNAME', 'drone')
# )

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'drone')
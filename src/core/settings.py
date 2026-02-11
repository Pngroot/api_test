import dotenv, os


dotenv.load_dotenv()


DB_URL = os.getenv('DB_URL') or None
ALEMBIC_DB_URL = os.getenv('ALEMBIC_DB_URL') or None
REDIS_URL = os.getenv('REDIS_URL') or None
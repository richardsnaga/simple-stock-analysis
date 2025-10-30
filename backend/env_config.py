import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

alembic_ini_path = "alembic.ini"

with open(alembic_ini_path, "r") as file:
    alembic_ini_content = file.read()

alembic_ini_content = alembic_ini_content.replace(
    "sqlalchemy.url = driver://user:pass@localhost/dbname", 
    f"sqlalchemy.url = {DATABASE_URL}"
)

with open(alembic_ini_path, "w") as file:
    file.write(alembic_ini_content)

print("alembic.ini telah diperbarui dengan DATABASE_URL dari .env")

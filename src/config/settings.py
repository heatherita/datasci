import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://heather:shinyHy3n%40@127.0.0.1:5432/analytics")
APP_NAME=os.getenv("APP_NAME", "Datascience cli app")
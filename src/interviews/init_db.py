from interviews.db.database import engine, Base
from sqlalchemy import text
# import your models so they register with Base. DO THIS
from interviews.db import models  # or wherever they live

# be sure to run this in psql first as su:
# GRANT USAGE, CREATE ON SCHEMA li TO heather;
def main():
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS li"))
        conn.commit()
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

if __name__ == "__main__":
    main()
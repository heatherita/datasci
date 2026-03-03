from interviews.client.li_interview import interview_script_2, interview_script_1, interview_script_4
from interviews.db.database import engine, Base
from sqlalchemy import text
# import your models so they register with Base. DO THIS
from interviews.db import models  # or wherever they live

# be sure to run this in psql first as su:
# GRANT USAGE, CREATE ON SCHEMA li TO heather;
def main():
    # interview_script_1()
    # interview_script_2()
    
    
    
    interview_script_4()


if __name__ == "__main__":
    main()
from interviews.client.li_interview import add_answers, add_questions, create_contacts, create_interviews, create_questions
from interviews.db.database import engine, Base
from sqlalchemy import text
# import your models so they register with Base. DO THIS
from interviews.db import models  # or wherever they live

# be sure to run this in psql first as su:
# GRANT USAGE, CREATE ON SCHEMA li TO heather;
def main():
   contacts = create_contacts()
   questions = create_questions()
   interviews = create_interviews()
   for interview in interviews:
       qas = add_questions(interview, questions)
       add_answers(qas)
   

if __name__ == "__main__":
    main()
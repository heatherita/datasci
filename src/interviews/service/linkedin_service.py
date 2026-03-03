
import time
from datetime import datetime, timezone

from interviews.db.database import SessionLocal
from interviews.db.models import Interview, LinkedInContact, Question, InterviewQA
from sqlalchemy import and_

db = SessionLocal()
def add_contact(firstname:str, lastname:str, title:str, company:str):
    contact = LinkedInContact(
        firstname=firstname,
        lastname=lastname,
        title=title,
        company=company
    )
    db.add(contact)
    db.commit()
    return contact

def add_question(question_text:str):
    question = Question(
        text=question_text
    )
    db.add(question)
    db.commit()
    return question


def get_question(question_text:str):
    question = db.query(Question).filter(Question.text==question_text).first()
    return question

def get_questions_like(question_text_match:str) -> list[Question]:
    questions = db.query(Question).filter(Question.text.like(f"%{question_text_match}%"))
    return questions

def delete_contact(contact_id:int):
    db.delete(LinkedInContact).where(id==contact_id)
    db.refresh()
    

def get_contact_by_id(contact_id:int):
    contact = db.query(LinkedInContact).filter_by(id=contact_id).first()
    return contact

def get_contact_by_fullname(firstname:str, lastname:str=None):
    print(f"getting contact by {firstname} and {lastname}")
    contact = db.query(LinkedInContact).filter(and_(firstname==firstname,lastname==lastname)).first()
    return contact

def get_contact_by_firstname(firstname:str):
    print(f"getting contact by {firstname}")
    contact = db.query(LinkedInContact).filter(firstname==firstname).first()
    return contact


def create_qa(question:Question,comments:str,interview:Interview):
    # question = Question(text=question_text)
    qa = InterviewQA(
        interview=interview,
        question=question,
        comments=comments if comments else None
    )
    db.add(qa)
    db.commit()
    return qa

def update_qa(qa:InterviewQA, answer_text:str, comments:str = None):
    qa.answer_text = answer_text
    if comments:
        qa.comments = comments
    db.commit()
    return qa

def create_interview(interview_date:datetime,interview_notes:str,interview_contact:LinkedInContact):
    interview = Interview(
        contact=interview_contact,
        # qas = qas,
        interview_date=interview_date,
        notes=interview_notes
    )
    db.add(interview)
    db.commit()
    return interview

def add_contact_to_interview(contact:LinkedInContact, interview: Interview):
    interview.contact = contact
    db.commit()
    return interview
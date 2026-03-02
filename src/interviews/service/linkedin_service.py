
import time
from datetime import datetime, timezone

from interviews.db.database import SessionLocal
from interviews.db.models import LinkedInContact, Question, InterviewQA

db = SessionLocal()
def add_contact(name:str, title:str, company:str):
    contact = LinkedInContact(
        name=name,
        title=title,
        company=company
    )
    db.add(contact)
    db.commit()
    return contact

def add_question(question_text:str):
    question = Question(text=question_text)
    qa = InterviewQA(
        question=question,
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
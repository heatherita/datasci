
import time
from datetime import datetime, timezone

from interviews.db.database import SessionLocal
from interviews.db.models import Interview, LinkedInContact, PainPoint, Question, InterviewQA
from sqlalchemy import and_

db = SessionLocal()
def add_contact(firstname:str, lastname:str, title:str, *, company:str=None, profile_id:str = None, org_size:int, region:str=None, industry:str = None, security_posture:str = None, adoption_readiness:str = None):
    contact = LinkedInContact(
        firstname=firstname,
        lastname=lastname,
        profile_id=profile_id,
        title=title,
        company=company,
        industry=industry,
        security_posture=security_posture,
        adoption_readiness=adoption_readiness
    )
    db.add(contact)
    db.commit()
    return contact

def add_question(question_text:str,question_label:str = None):
    question = Question(
        text=question_text,
        label=question_label
    )
    db.add(question)
    db.commit()
    return question


def get_question_by_text(question_text:str):
    question = db.query(Question).filter(Question.text==question_text).first()
    return question

def get_question_by_label(question_label:str):
    question = db.query(Question).filter(Question.label==question_label).first()
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
    contact = db.query(LinkedInContact).filter(and_(LinkedInContact.firstname==firstname,LinkedInContact.lastname==lastname)).first()
    return contact

def get_contact_by_firstname(firstname:str):
    print(f"getting contact by {firstname}")
    contact = db.query(LinkedInContact).filter(LinkedInContact.firstname==firstname).first()
    return contact

def get_contact_by_profile_id(profile_id_in:str):
    print(f"getting contact by {profile_id_in}")
    contact = db.query(LinkedInContact).filter(LinkedInContact.profile_id==profile_id_in).first()
    return contact

def get_interview(interview_date_str:str,interview_contact:LinkedInContact) -> bool:
    try:
        interview_dt = datetime.strptime(interview_date_str, "%Y-%m-%d")  # Y-m-d
    except ValueError:
        raise ValueError("date_str must be in YYYY-MM-DD format")
    interview = db.query(Interview).filter(and_(Interview.contact_id==interview_contact.id,
                                                Interview.interview_date==interview_dt)).first()
    return interview


def create_interview(interview_date_str:str,interview_notes:str,interview_contact:LinkedInContact):
    try:
        interview_dt = datetime.strptime(interview_date_str, "%Y-%m-%d")  # Y-m-d
    except ValueError:
        raise ValueError("date_str must be in YYYY-MM-DD format")
    interview = Interview(
        contact=interview_contact,
        # qas = qas,
        interview_date=interview_dt,
        notes=interview_notes
    )
    db.add(interview)
    db.commit()
    return interview

def get_qa_in_interview(question:Question, interview:Interview):
    qa = db.query(InterviewQA).filter(
        and_(InterviewQA.interview_id==interview.id,
        InterviewQA.question_id==question.id)).first()
    return qa

def add_contact_to_interview(contact:LinkedInContact, interview: Interview):
    interview.contact = contact
    db.commit()
    return interview

def add_qa_to_interview(qa:InterviewQA, interview:Interview):
    interview.qas.append(qa)
    db.commit()    
    return interview

def create_qa(question:Question,interview:Interview, *, comments:str = None, answer_text:str = None):
    # question = Question(text=question_text)
    qa = InterviewQA(
        interview=interview,
        question=question,
        comments=comments,
        answer_text=answer_text
    )
    db.add(qa)
    db.commit()
    return qa

def add_answer_to_qa(qa:InterviewQA, answer_text:str):
    qa.answer_text = answer_text
    db.commit()
    return qa

def add_answer(question_text:str, answer_text:str, interview:Interview):
    try:
        question = get_question(question_text)
        qa = get_qa_in_interview(question, interview)
        qa.answer_text = answer_text
        db.commit()
        return qa
        
    except ValueError:
        error = f"can't add answer {answer_text} to question: {question_text} for profile: {profile_id}"
        raise ValueError(error)   
    
    

def create_pain_point(pp_text:str, interview:Interview):
    painpoint = PainPoint(
        text=pp_text
    )
    db.add(painpoint)
    db.commit()
    return painpoint



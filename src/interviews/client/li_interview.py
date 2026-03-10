
import json
from pathlib import Path
from interviews.db.models import Interview, InterviewQA, PainPoint, Question
from interviews.service.linkedin_service import add_answer_to_qa, add_contact, add_contact_to_interview, add_question, create_interview, create_pain_point, create_qa, delete_contact, get_contact_by_firstname, get_contact_by_fullname, get_contact_by_id, get_contact_by_profile_id, get_interview, get_pain_point_by_text, get_pain_point_in_interview, get_qa_in_interview, get_question_by_label, get_question_by_text, get_questions_like
from datetime import datetime


        
def create_contacts():
    contacts = []
    interview_path = Path(__file__).resolve().parents[1] / "json" / "dummy-20260303.json"
    with interview_path.open() as f:
        interviews_json = json.load(f)

    #add contacts
    for ij in interviews_json:
        contact = get_contact_by_profile_id(ij["profile_id"])
        if contact:
            print(f"CONTACT EXISTS {contact.profile_id} with lastname {contact.lastname}")
        else:
            contact = add_contact(
                firstname=ij["name"].split(" ")[0],
                lastname=ij["name"].split(" ")[1],
                title=ij["title"],
                industry=ij["industry"],
                profile_id=ij["profile_id"],            
                org_size=ij["org_size"],            
                region=ij["region"],            
                security_posture=ij["security_posture"],            
                adoption_readiness=ij["adoption_readiness"]            
                )
        contacts.append(contact)
    print(f"finished adding {len(interviews_json)} contacts")  
    return contacts
    
#add questions
def create_questions():
    questions = []
    questions_path = Path(__file__).resolve().parents[1] / "json" / "li_questions_20260303.json"
    with questions_path.open() as f:
        questions_json = json.load(f)
        for question_json in questions_json:
            question = get_question_by_label(question_json["question_label"])
            if question:
                print(f"QUESTION EXISTS with text: {question.label} and {question.text}")
            else:
                add_question(question_json["question_text"],question_json["question_label"])
            questions.append(question)
    return questions

def create_pain_points():
    pps = []
    interview_path = Path(__file__).resolve().parents[1] / "json" / "dummy-20260303.json"
    with interview_path.open() as f:
        interviews_json = json.load(f)
        for ij in interviews_json:
            pain_points = ij["top_pains"]
            for pp_str in pain_points:
                pp = get_pain_point_by_text(pp_str)
                if pp:
                    print(f"PAIN POINT EXISTS with text: {pp.text}")
            else:
                pp = create_pain_point(pp_str)
            pps.append(pp)
    return pps
                    

def create_interviews():  
    interviews = []     
    interview_path = Path(__file__).resolve().parents[1] / "json" / "dummy-20260303.json"
    with interview_path.open() as f:
        interviews_json = json.load(f)

    #add contacts
    for ij in interviews_json:
        contact = get_contact_by_profile_id(ij["profile_id"])
        if contact:
            print(f"CONTACT EXISTS {contact.profile_id} with lastname {contact.lastname}")
            interview = get_interview(ij["interview_date"],contact)
            if interview:
                print(f"INTERVIEW EXISTS for {contact.firstname} {contact.lastname} and date {interview.interview_date}") 
            else:
                interview = create_interview(ij["interview_date"],"initial linkedin interview", contact) 
            interviews.append(interview)
    return interviews

def add_questions(interview:Interview, questions:list[Question]):
    qas = []
    for question in questions:
        print(f"QUESTION ITERATED: {question.id} {question.text}")
        qa = get_qa_in_interview(question,interview)
        if qa:
            print(f"QA EXISTS with text: {question.text} for interview: {interview.notes} from {interview.interview_date}")
        else:
            qa = create_qa(question, interview)
            print(f"ADDED QA with text: {question.text} for interview: {interview.notes} from {interview.interview_date}")
        qas.append(qa)
    return qas

def add_pain_points(interview:Interview, pain_points:list[PainPoint]):
    # pps = []
    for pp in pain_points:
        print(f"PAIN POINT ITERATED: {pp.id} {pp.text}")
        pp = get_pain_point_in_interview(interview, pain_points)
        if pp:
             print(f"PAIN POINT EXISTS with text: {pp.text} for interview: {interview.notes} from {interview.interview_date}")
        else:
            pp = add_pain_point(interview, )
            print(f"ADDED QA with text: {question.text} for interview: {interview.notes} from {interview.interview_date}")
        qas.append(qa)
            
        

def add_answers(qas:list[InterviewQA]):
    interview_path = Path(__file__).resolve().parents[1] / "json" / "dummy-20260303.json"
    with interview_path.open() as f:
        interviews_json = json.load(f)
        for ij in interviews_json:

            for qa in qas:
                question:Question = qa.question
                # answer_text = ij[question.label]
                add_answer_to_qa(qa, ij[question.label])
                
        

def add_answers_scratch():
    interview_path = Path(__file__).resolve().parents[1] / "json" / "dummy-20260303.json"
    with interview_path.open() as f:
        interviews_json = json.load(f)
        field_names = interviews_json.keys()      
        #add contacts
        for ij in interviews_json:
            contact = get_contact_by_profile_id(ij["profile_id"])
            if contact:
                interview = get_interview(ij["interview_date"],contact)
                if interview:
                    print(f"INTERVIEW EXISTS for {contact.firstname} {contact.lastname} and date {interview.interview_date}") 
                    for field_name in field_names:
                        question = get_question_by_label(field_name)
                        if question:
                            qa = get_qa_in_interview(question, interview)
                            if qa:
                                add_answer_to_qa(qa, ij[field_name])
        
                    
          
        
    


import json
from pathlib import Path

from interviews.service.linkedin_service import add_contact, add_contact_to_interview, add_question, create_interview, create_qa, delete_contact, get_contact_by_firstname, get_contact_by_fullname, get_contact_by_id, get_contact_by_profile_id, get_question, get_questions_like
from datetime import datetime



def interview_script_1():
    
    contact = add_contact("mary","ronstandt","purchaser","miele")
    print(f"the contact is {contact}")
    add_question("how big are your feet?")
    add_question("how hip are your friends?")
    add_question("how long can you dance?")
    add_question("how big is your dog?")
    questions = get_questions_like("how big")
    for ques in questions:
        print(f"the question is {ques.id} and {ques.text}")
        
    
def interview_script_2():
    
    contact = get_contact_by_fullname("mary","ronstandt")
    print(f"the contact is {contact}")

    # questions = []
    # questions.append(get_question("how big are your feet?"))
    # questions.append(get_question("how hip are your friends?"))
    # questions.append(get_question("how long can you dance?"))
    # questions.append(get_question("how big is your dog?"))
    
    question1 = get_question("how big are your feet?")
    question2 = get_question("how hip are your friends?")
    question3 = get_question("how long can you dance?")
    question4 = get_question("how big is your dog?")

    qas = []
    
    interview_date = datetime.strptime("2026-03-03", "%Y-%m-%d")
    interview = create_interview(interview_date, "here are some notes",contact)
    # interview = add_contact_to_interview(contact,interview) 
    qas.append(create_qa(question1,"this is the first question",interview))
    qas.append(create_qa(question2,"this is the second question",interview))
    qas.append(create_qa(question3,"yes, the third question",interview))
    qas.append(create_qa(question4,"and yes yes yes, the fourth question",interview))
    return interview              


def interview_script_3():
    
    contact = get_contact_by_firstname("mary")
    if contact:
        print(f"deleting contact with name: {contact.firstname} {contact.lastname} and id: {contact.id}")
        delete_contact(contact.id)
        print(f"contact is deleted")
        
def interview_script_4():
    interview_path = Path(__file__).resolve().parents[1] / "json" / "dummy-20260303.json"
    with interview_path.open() as f:
                interviews_json = json.load(f)


    for ij in interviews_json:
        contact = get_contact_by_profile_id(ij["profile_id"])
        if contact:
            print(f"contact {contact.profile_id} with lastname {contact.lastname} already exists")
        else:
            add_contact(
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
    print(f"finished adding {len(interviews_json)} contacts")    

        
    

SELECT contact.id AS "contact id"
    , contact.firstname
    , contact.lastname
    , interview.id AS "interview id"
    , interview.interview_date
    , interview.notes
    , question.text
    , question.id AS "question id"
    , interview_qa.id AS "qa id"
    , interview_qa.answer_text
    , interview_qa.comments
FROM li.interview LEFT OUTER JOIN li.interview_qa
    ON li.interview.id = interview_id LEFT OUTER JOIN li.question
    ON li.question.id = question_id LEFT OUTER JOIN li.contact
    ON li.contact.id = contact_id

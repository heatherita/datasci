from enum import UNIQUE

from sqlalchemy import Column, Integer, Float, String, Text, DateTime, Boolean, Date, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from interviews.db.database import Base

class LinkedInContact(Base):
    __tablename__ = "contact"
    __table_args__ = {"schema": "li"}

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    title = Column(String)
    company = Column(String)
    industry = Column(String)
    org_size = Column(String)
    region = Column(String)    
    security_posture = Column(String)
    adoption_readiness = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    fetched_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    interviews = relationship("Interview", back_populates="contact",lazy="selectin")

class Interview(Base):
    __tablename__ = "interview"
    __table_args__ = {"schema": "li"}

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("li.contact.id",ondelete="SET NULL"),nullable=True)
    notes = Column(Text)
    interview_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    fetched_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    contact = relationship("LinkedInContact", back_populates="interviews",lazy="selectin")
    qas = relationship("InterviewQA", back_populates="interview", lazy="selectin", cascade="all, delete-orphan")
    painpoints = relationship("PainPoint", back_populates="interview", lazy="selectin", cascade="all, delete-orphan")


class InterviewQA(Base):
    __tablename__ = "interview_qa"
    __table_args__ = {"schema": "li"}
    __table_args__ = (
        UniqueConstraint("interview_id", "question_id", name="uq_interviewqa_interview_question"),
        {"schema": "li"},
    )
    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(
        Integer,
        ForeignKey("li.interview.id", ondelete="CASCADE"),
        nullable=False,
    )
    question_id = Column(Integer, ForeignKey("li.question.id",ondelete="SET NULL"), nullable=True)
    answer_text = Column(Text)
    comments = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    fetched_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    question = relationship("Question", back_populates="qas",lazy="selectin")
    interview = relationship("Interview", back_populates="qas",lazy="selectin")
    metrics = relationship("AnswerSentiment", back_populates="qa",lazy="selectin", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "question"
    __table_args__ = {"schema": "li"}

    id = Column(Integer, primary_key=True)
    label = Column(String, unique=True, nullable=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    fetched_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    qas = relationship("InterviewQA", back_populates="question",lazy="selectin", cascade="all, delete-orphan")
    
    
class PainPoint(Base):
    __tablename__ = "pain_point"
    __table_args__ = {"schema": "li"}

    id = Column(Integer, primary_key=True)
    interview_id = Column(
        Integer, ForeignKey("li.interview.id"), nullable=False,
    )
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    fetched_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    interview = relationship("Interview", back_populates="painpoints",lazy="selectin")
    



class AnswerSentiment(Base):
    __tablename__ = "answer_sentiment"
    __table_args__ = {"schema": "li"}

    id = Column(Integer, primary_key=True)
    interview_qa_id = Column(Integer, ForeignKey("li.interview_qa.id"), nullable=False)

    model = Column(String(100), nullable=False)   # e.g. "vader", "textblob", "gpt-..."
    polarity = Column(Float)
    subjectivity = Column(Float)
    compound = Column(Float)
    pos = Column(Float)
    neu = Column(Float)
    neg = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    qa = relationship("InterviewQA",back_populates="metrics",lazy="selectin")







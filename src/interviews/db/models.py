from enum import UNIQUE

from sqlalchemy import Column, Integer, Float, String, Text, DateTime, Boolean, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from interviews.db.database import Base

class LinkedInContact(Base):
    __tablename__ = "contact"
    __table_args__ = {"schema": "li"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    title = Column(Text)
    company = Column(Text)
    industry = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    fetched_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    interviews = relationship("Interview", back_populates="contact")

class Interview(Base):
    __tablename__ = "interview"
    __table_args__ = {"schema": "li"}

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("li.contact.id"), nullable=False)
    notes = Column(Text)
    interview_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    fetched_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    contact = relationship("LinkedInContact", back_populates="interviews")
    qas = relationship("InterviewQA", back_populates="interview", cascade="all, delete-orphan")


class InterviewQA(Base):
    __tablename__ = "interview_qa"
    __table_args__ = {"schema": "li"}
    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("li.interview.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("li.question.id"), nullable=False)
    answer_text = Column(Text)
    comments = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    fetched_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    question = relationship("Question", back_populates="qas")
    interview = relationship("Interview", back_populates="qas")


class Question(Base):
    __tablename__ = "question"
    __table_args__ = {"schema": "li"}

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    fetched_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    qas = relationship("InterviewQA", back_populates="question")

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

    qa = relationship("InterviewQA")







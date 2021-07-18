from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class SocialCreditDatabase(Base):
    __tablename__ = 'social_credit_users'
    id = Column(Integer, primary_key=True)
    rating = Column(Integer)
    username = Column(String(255))

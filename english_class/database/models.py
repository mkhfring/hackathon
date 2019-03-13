from sqlalchemy import Column, String, Integer, ForeignKey

from english_class.database.connect import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    user_id = Column(String)


class FileInformation(Base):
    __tablename__ = "file_information"
    id = Column(Integer, primary_key=True)
    file_id = Column(String)
    owner_id = Column(String, ForeignKey('user.user_id'))
    witting_owner_name = Column(String, nullable=True)


class Quiz(Base):
    __tablename__ = 'quiz'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    option_1 = Column(String)
    option_2 = Column(String)
    option_3 = Column(String)
    option_4 = Column(String)
    answer = Column(Integer)


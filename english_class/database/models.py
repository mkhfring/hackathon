from sqlalchemy import Column, String, Integer, ForeignKey, Boolean

from english_class.database.connect import Base, session


class User(Base):
    __tablename__ = "user"
    id = Column(String, primary_key=True)
    name = Column(String)

    @classmethod
    def is_exist(cls, user_id):
        return session.query(cls).filter(cls.user_id == user_id).one_or_none()


class FileInformation(Base):
    __tablename__ = "file_information"
    id = Column(Integer, primary_key=True)
    file_id = Column(String)
    owner_id = Column(String, ForeignKey('user.id'))
    witting_owner_name = Column(String, nullable=True, default=None)
    is_sent = Column(Boolean, default=False)


class Quiz(Base):
    __tablename__ = 'quiz'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    option_1 = Column(String)
    option_2 = Column(String)
    option_3 = Column(String)
    option_4 = Column(String)
    answer = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))
    is_sent = Column(Boolean)


class UserQuiz(Base):
    __tablename__ = 'user_quiz'

    quiz_id = Column(Integer, ForeignKey('Quiz.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'), primary_key=True)


class UserInformation(Base):
    __tablename__ = 'information_quiz'

    information_id = Column(Integer, ForeignKey('FileInformation.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'), primary_key=True)

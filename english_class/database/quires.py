# In the name of God
from sqlalchemy.exc import SQLAlchemyError

import logging

from english_class.constants.messages import LogMessage
from english_class.database import connect
from english_class.database.models import User, FileInformation, UserQuiz, Quiz

session = connect.session_factory()

logger = logging.getLogger()


def db_persist(func):
    def persist(*args, **kwargs):
        func(*args, **kwargs)
        try:
            session.commit()
        except SQLAlchemyError as e:
            logger.info(LogMessage.db_error.format(e, func.__name__))
            session.rollback()
            return False

    return persist


@db_persist
def add_user(user_id):
    if not User.is_exist(user_id=user_id):
        user = User(user_id=user_id)
        session.add(user)


def get_all_not_sent_information():
    return session.query(FileInformation).filter(FileInformation.is_sent is False).filter(
        FileInformation.witting_owner_name is None).first()


@db_persist
def update_is_sent_status(file_id):
    info = session.query(FileInformation).filter(FileInformation.file_id == file_id).one_or_none()
    info.is_sent = True


@db_persist
def save_writing(writing_file, owner_id):
    owner = session(User).filter(User.user_id == owner_id).one_or_none()
    file = FileInformation(file_id=writing_file.file_id, owner_id=owner.user_id,
                           witting_owner_name=owner.name)
    session.add(file)


@db_persist
def get_user_related_quiz(user_id):
    quiz_id = session.query(UserQuiz).filter(UserQuiz.user_id == user_id).one_or_none()

    if not quiz_id:
        quiz_id = 1

    quiz = session.query(Quiz).filter(Quiz.id == quiz_id)

    quiz_id += 1

    user_quiz = UserQuiz(quiz_id=quiz_id, user_id=user_id)

    session.merge(user_quiz)

    return quiz

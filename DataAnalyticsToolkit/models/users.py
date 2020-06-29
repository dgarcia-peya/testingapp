from sqlalchemy import Column, Integer, String, Boolean
from DataAnalyticsToolkit.database import MysqlBase


class User(MysqlBase):
    __tablename__ = 'Users'
    email = Column(String)
    role = Column(Integer)
    is_active = Column(Boolean)
    is_authenticated = Column(Boolean)
    is_anonymous = Column(Boolean)
    __mapper_args__ = {
        'primary_key': [email]
    }

    @staticmethod
    def get(user_email):
        user = User.query.get(user_email)
        return user

    def get_id(self):
        return self.email

    def __repr__(self):
        return f'<User {self.email}>'

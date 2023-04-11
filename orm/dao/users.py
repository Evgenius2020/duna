from dataclasses import asdict
from typing import Union

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from tables import User, engine


class UsersDAO:
    @staticmethod
    def register(name: str) -> Union[User, None]:
        with Session(engine) as sess:
            user = User(name=name)
            try:
                sess.add(user)
                sess.commit()
            except IntegrityError:
                # When user.name is not unique:
                return None
            return User(**asdict(user))


if __name__ == '__main__':
    u = UsersDAO.register('u7')
    print(u)

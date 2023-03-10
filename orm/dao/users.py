from typing import Union

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from tables import User, engine, Base


def convert_insert_result_to_object(obj,
                                    target_type: Base) -> Base:
    fields = obj.__dict__
    del fields['_sa_instance_state']
    return target_type(**fields)


class UsersDAO:
    @staticmethod
    def register(name: str) -> Union[User, None]:
        with Session(engine) as sess:
            user = User(name=name)
            try:
                sess.add(user)
                sess.commit()
            except IntegrityError as e:
                # When user.name is not unique:
                return None
            return convert_insert_result_to_object(user, User)


if __name__ == '__main__':
    u = UsersDAO.register('u5')
    print(u)

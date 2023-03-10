import enum
import os
from datetime import datetime

from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        String, create_engine)

from sqlalchemy.orm import (Session, declarative_base, mapped_column,
                            relationship)

Base = declarative_base()
# TODO: aiopg, asyncpgsa - async engines.
engine = create_engine(os.getenv('db_url'))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)
    is_bot = Column(Boolean, nullable=False, default=False)


class GameStatus(enum.Enum):
    unfinished = 0,
    host_win = 1,
    guest_win = 2


class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)

    host_id = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    host = relationship('User', foreign_keys=host_id)
    guest_id = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    guest = relationship('User', foreign_keys=[guest_id])
    host_played_first = Column(Boolean(), nullable=False)

    started_at = Column(DateTime(timezone=True), default=datetime.now())
    finished_at = Column(DateTime(timezone=True))

    # TODO: Temp variables. Maybe move them to a temp storage?
    board_state = Column(String(length=169), default='e' * 169)
    host_current_turn = \
        Column(Boolean(),
               default=lambda context:
               context.get_current_parameters()['host_played_first'])

    history = Column(String())
    result = Column(Enum(GameStatus), default=GameStatus.unfinished)


if __name__ == '__main__':
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)
    sess = Session(engine)
    # user1 = User(name='user1')
    # user2 = User(name='user2')
    user1 = sess.query(User).filter(User.name == 'user1').first()
    user2 = sess.query(User).filter(User.name == 'user2').first()
    game = Game(host=user1,
                guest=user2,
                host_played_first=False)
    sess.add_all([user1, user2, game])
    sess.commit()

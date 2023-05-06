import enum
import os
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)
from sqlalchemy.orm import Session, registry

metadata = MetaData()
# TODO: aiopg, asyncpgsa - async engines.
engine = create_engine(os.getenv('db_url'))


class GameStatus(enum.Enum):
    unfinished = 0
    host_win = 1
    guest_win = 2


@dataclass
class User:
    id: int = None
    name: str = ''
    is_bot: bool = False


@dataclass
class Game:
    id: int = None

    host_id: int = None
    guest_id: int = None
    host_played_first: bool = True

    started_at: datetime = datetime.now()
    ended_at: datetime = None
    history: str = ''

    # TODO: Temp variable. Maybe move them to a temp storage?
    host_current_turn: bool = host_played_first

    result: GameStatus = GameStatus.unfinished


mapper_registry = registry(metadata=metadata)
mapper_registry.map_imperatively(
    User,
    Table(
        'user',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(30), nullable=False, unique=True),
        Column('is_bot', Boolean, nullable=False, default=False),
    ),
)
mapper_registry.map_imperatively(
    Game,
    Table(
        'game',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('host_id', Integer, ForeignKey('user.id'), nullable=False),
        Column('guest_id', Integer, ForeignKey('user.id'), nullable=False),
        Column('host_played_first', Boolean, nullable=False),
        Column('started_at', DateTime(timezone=True), nullable=False),
        Column('ended_at', DateTime(timezone=True), nullable=True),
        Column('history', String, nullable=False),
        Column('host_current_turn', Boolean, nullable=False),
        Column('result', Enum(GameStatus), nullable=False),
    ),
)

if __name__ == '__main__':
    sess = Session(engine)
    user1 = sess.query(User).filter(User.name == 'user1').first()
    user2 = sess.query(User).filter(User.name == 'user2').first()
    game = Game(host_id=user1.id, guest_id=user2.id)
    sess.add_all([user1, user2, game])
    sess.commit()
    print(sess.query(Game).all())

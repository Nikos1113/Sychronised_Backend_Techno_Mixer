import sqlalchemy
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, sessionmaker
from pydantic import BaseModel

app = FastAPI()

DB_URL = "sqlite:///./songs.db"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()


class SongTable(Base):
    """Represents a song record stored in the database."""

    __tablename__ = "table_for_songs"

    song_id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    artist: str = Column(String, index=True)
    bpm: int = Column(Integer)


class SongPart(Base):
    """Represents a section or part of a song."""

    __tablename__ = "parts_of_songs"

    part_id: int = Column(Integer, primary_key=True, index=True)
    start_time: str = Column(String)
    end_time: str = Column(String)
    song_id: int = Column(Integer, ForeignKey("table_for_songs.song_id"))


Base.metadata.create_all(bind=engine)


def get_db():
    """Provide a database session and close it after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class SongItem(BaseModel):
    """Schema for adding a song to the database."""

    song_name: str
    song_artist: str
    song_bpm: int
    song_id: int


@app.post("/add_a_song")
def add_an_item(song: SongItem, db: Session = Depends(get_db)):
    """Add a song record to the database."""
    db_song = SongTable(
        name=song.song_name,
        artist=song.song_artist,
        bpm=song.song_bpm
    )
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song
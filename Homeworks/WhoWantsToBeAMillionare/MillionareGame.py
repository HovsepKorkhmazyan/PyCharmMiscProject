import os
import csv
import random
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./questions.db"
DB_EXISTS = os.path.exists("questions.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)
    option1 = Column(String)
    option2 = Column(String)
    option3 = Column(String)
    option4 = Column(String)

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    score = Column(Integer)

class QuestionCreate(BaseModel):
    question_text: str
    correct_answer: str
    wrong_answer_1: str
    wrong_answer_2: str
    wrong_answer_3: str

class GameStart(BaseModel):
    username: str

class GameQuestion(BaseModel):
    id: int
    question_text: str
    answers: List[str]

    class Config:
        orm_mode = True

class AnswerCheck(BaseModel):
    question_id: int
    answer: str

class PlayerCreate(BaseModel):
    name: str
    score: int

class PlayerScore(BaseModel):
    name: str
    score: int

    class Config:
        orm_mode = True

app = FastAPI(
    title="Who want to be a millionare",
    description="An API for a simple quiz game using FastAPI and SQLite.",
    version="1.0.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    if not DB_EXISTS:
        db = SessionLocal()
        try:
            with open('questions.csv', 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                questions_to_add = []
                for row in reader:
                    if len(row) == 5:
                        questions_to_add.append(
                            Question(
                                question_text=row[0],
                                option1=row[1],
                                option2=row[2],
                                option3=row[3],
                                option4=row[4],
                            )
                        )
                db.add_all(questions_to_add)
                db.commit()
        except FileNotFoundError:
            print("WARNING: questions.csv not found. Database will be initialized empty.")
        except Exception as e:
            print(f"An error occurred while reading questions.csv: {e}")
            db.rollback()
        finally:
            db.close()

@app.post("/game", response_model=List[GameQuestion], summary="Start a new game")
def start_game(payload: GameStart, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.name == payload.username).first()
    if not player:
        new_player = Player(name=payload.username, score=0)
        db.add(new_player)
        db.commit()

    random_questions = db.query(Question).order_by(func.random()).limit(10).all()

    if not random_questions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No questions found in the database. Please add some questions first."
        )

    game_questions = []
    for q in random_questions:
        answers = [q.option1, q.option2, q.option3, q.option4]
        random.shuffle(answers)
        game_questions.append(
            GameQuestion(id=q.id, question_text=q.question_text, answers=answers)
        )
    return game_questions


@app.post("/add_question", status_code=status.HTTP_201_CREATED, summary="Add a new question")
def add_question(question: QuestionCreate, db: Session = Depends(get_db)):
    new_question = Question(
        question_text=question.question_text,
        option1=question.correct_answer,
        option2=question.wrong_answer_1,
        option3=question.wrong_answer_2,
        option4=question.wrong_answer_3,
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return {"message": "Question added successfully!", "question_id": new_question.id}


@app.post("/check_answer", summary="Check an answer")
def check_answer(payload: AnswerCheck, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == payload.question_id).first()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with ID {payload.question_id} not found."
        )

    is_correct = (question.option1 == payload.answer)
    return {"correct": is_correct, "correct_answer": question.option1}


@app.post("/scores", status_code=status.HTTP_200_OK, summary="Submit a player's score")
def submit_score(player: PlayerCreate, db: Session = Depends(get_db)):
    existing_player = db.query(Player).filter(Player.name == player.name).first()

    if not existing_player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player '{player.name}' not found. A game must be started with a username before submitting a score."
        )

    if player.score > existing_player.score:
        existing_player.score = player.score
        db.commit()
        db.refresh(existing_player)
        return {"message": f"New high score for {player.name} ({player.score}) has been recorded."}

    return {"message": f"Your score ({player.score}) was not higher than your current high score ({existing_player.score})."}


@app.get("/leaderboard", response_model=List[PlayerScore], summary="Get top player scores")
def get_leaderboard(limit: int = 10, db: Session = Depends(get_db)):
    top_players = db.query(Player).order_by(Player.score.desc()).limit(limit).all()
    return top_players


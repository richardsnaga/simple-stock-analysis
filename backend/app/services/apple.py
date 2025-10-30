from sqlalchemy.orm import Session
from app.models.apple import Apple
from app.schemas.apple import AppleCreate

def create_apple(db: Session, apple: AppleCreate):
    db_apple = Apple(date=apple.date, price=apple.price, open=apple.open, high=apple.high, low=apple.low, vol=apple.vol)
    db.add(db_apple)
    db.commit()
    db.refresh(db_apple)
    return db_apple

def get_apples(db: Session):
    return db.query(Apple).order_by(Apple.id.asc()).all()
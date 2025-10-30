from sqlalchemy.orm import Session
from app.models.google import Google

def get_googles(db: Session):
    return db.query(Google).order_by(Google.id.asc()).all()
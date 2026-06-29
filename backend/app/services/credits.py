from sqlalchemy.orm import Session
from ..models.user import User

def deduct_credits(db: Session, user: User, amount: int) -> bool:
    if user.credits >= amount:
        user.credits -= amount
        db.commit()
        db.refresh(user)
        return True
    return False

def get_balance(user: User) -> int:
    return user.credits

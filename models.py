from sqlalchemy import Column, Integer, String, DateTime, func
from .database import Base


class IntakeLog(Base):
    __tablename__ = "intake_logs"

    id = Column(Integer, primary_key=True, index=True)
    amount_ml = Column(Integer, nullable=False)
    note = Column(String, nullable=True)
    logged_at = Column(DateTime, default=func.now(), server_default=func.now())

    def __repr__(self):
        return f"<IntakeLog id={self.id} amount={self.amount_ml}ml at={self.logged_at}>"

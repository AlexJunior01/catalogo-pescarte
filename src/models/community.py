import uuid
from typing import List

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.base_sql_model import BaseSQLModel
from src.database import BaseModel, Session


class Community(BaseModel, BaseSQLModel):
    __tablename__ = 'community'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    municipality_id = Column(UUID(as_uuid=True), ForeignKey('municipality.id'))

    # Relationship - each Community is related to a Municipality
    municipality = relationship("Municipality", back_populates="communities")
    fish_common_names = relationship("FishCommonNameByCommunity", back_populates="community")
    suggested_names = relationship("SuggestedCommonNames", back_populates="community")

    @classmethod
    def get_all(cls, db: Session) -> List["Community"]:
        return db.query(cls).all()

    @classmethod
    def get_by_id(cls, db: Session, gear_id: UUID) -> "Community":
        return db.query(cls).filter_by(id=gear_id).first()

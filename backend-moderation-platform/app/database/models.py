from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean, SmallInteger
from sqlalchemy.orm import relationship
from app.database.connection import Base


# Tables
class Region(Base):
    __tablename__ = 'tb_regions'
    region_id = Column(Integer, primary_key=True)
    region_code = Column(String(10))
    region_name = Column(String(50))

class EventCategory(Base):
    __tablename__ = 'tb_event_categories'
    category_id = Column(Integer, primary_key=True)
    category_code = Column(String(10))
    category_name = Column(String(50))

class Moderator(Base):
    __tablename__ = 'tb_moderator'
    moderator_id = Column(Integer, primary_key=True, autoincrement=True)
    moderator_name = Column(String(8), unique=True)
    moderator_region_id = Column(Integer, ForeignKey('tb_regions.region_id'))
    region = relationship("Region")



class Event(Base):
    __tablename__ = 'tb_events'
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('tb_event_categories.category_id'))
    region_id = Column(Integer, ForeignKey('tb_regions.region_id'))
    event_title = Column(String(100))
    event_description = Column(Text)
    claimed_status = Column(SmallInteger, nullable=False, default=0)
    category = relationship("EventCategory")
    region = relationship("Region")

class Assignment(Base):
    __tablename__ = 'tb_assignment'
    assignment_id = Column(Integer, primary_key=True)
    moderator_id = Column(Integer, ForeignKey('tb_moderator.moderator_id'))
    event_id = Column(Integer, ForeignKey('tb_events.event_id'))
    claimed_time = Column(DateTime(timezone=True), nullable=False)
    expire_time = Column(DateTime)
    ack_status = Column(SmallInteger, nullable=False, default=0)
    ack_time = Column(DateTime(timezone=True))
    moderator = relationship("Moderator")
    event = relationship("Event")

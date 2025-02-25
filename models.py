from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Talent(Base):
    __tablename__ = 'talents'

    id = Column(String, primary_key=True)
    talent_name = Column(String)
    talent_grade = Column(String)
    booking_grade = Column(String)
    operating_unit = Column(String, nullable=False)
    office_city = Column(String)
    office_postal_code = Column(String, nullable=False)

    planners = relationship("Planner", backref="associated_talent")


class JobManager(Base):
    __tablename__ = 'job_managers'

    id = Column(String, primary_key=True)
    job_manager_name = Column(String)

    planners = relationship("Planner", backref="associated_job_manager")


class Client(Base):
    __tablename__ = 'clients'

    id = Column(String, primary_key=True)
    client_name = Column(String)
    industry = Column(String)
    is_unassigned = Column(Boolean)

    planners = relationship("Planner", backref="associated_client")


class Skill(Base):
    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True)
    skill_name = Column(String)
    skill_category = Column(String)

    skill_associations = relationship('PlannerSkillAssociation', back_populates='skill')


class PlannerSkillAssociation(Base):
    __tablename__ = 'client_skill_association'

    id = Column(Integer, primary_key=True)
    planner_id = Column(String, ForeignKey('planners.id'))
    skill_id = Column(Integer, ForeignKey('skills.id'))
    mandatory = Column(Boolean, default=False)
    planner = relationship('Planner', back_populates='planner_associations')
    skill = relationship('Skill', back_populates='skill_associations')


class Planner(Base):
    __tablename__ = 'planners'

    id = Column(Integer, primary_key=True)
    original_id = Column(String, unique=True, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'))
    talent_id = Column(Integer, ForeignKey('talents.id'))
    job_manager_id = Column(Integer, ForeignKey('job_managers.id'))
    total_hours = Column(Float, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    client = relationship("Client", back_populates="planners", overlaps="associated_client")
    talent = relationship("Talent", back_populates="planners", overlaps="associated_talent")
    job_manager = relationship("JobManager", back_populates="planners", overlaps="associated_job_manager")
    planner_associations = relationship('PlannerSkillAssociation', back_populates='planner')

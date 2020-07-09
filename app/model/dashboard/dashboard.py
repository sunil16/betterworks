# -*- coding: utf-8 -*-
from sqlalchemy import ForeignKey, Column, func, create_engine, MetaData, Table, Column, Integer, String,DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
import datetime

from app.model import Base
from app.utils import alchemy

class Department(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=True)
    location = Column(String(20), nullable=True)
    date_of_innaugration = Column(DateTime, nullable=True)
    team = relationship("Team")

    def __repr__(self):
        return "<Department(id='%s',name='%s')>" % (
            self.id,
            self.name
        )

    FIELDS = { "id":int, "name": str}

class Team(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_lead_id = Column(Integer, nullable=True)
    average_pay = Column(String(20), nullable=True)
    department_id = Column(Integer, ForeignKey('department.id'))
    user = relationship("User")

    def __repr__(self):
        return "<Team(id='%s',team_lead_id='%s',average_pay='%s',department_id='%s')>" % (
            self.id,
            self.team_lead_id,
            self.average_pay,
            self.department_id
        )

    FIELDS = {"average_pay": str,"average_pay": str, "department_id":int}

class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_Name = Column(String(20), nullable=True)
    last_Name = Column(String(20), nullable=True)
    team_id = Column(Integer, ForeignKey('team.id'))
    objective = relationship("Objective")

    def __repr__(self):
        return "<User(id='%s',first_Name='%s',last_Name='%s',team_id='%s')>" % (
            self.id,
            self.first_Name,
            self.last_Name,
            self.team_id
        )

    FIELDS = {"first_Name": str,"last_Name": str, "team_id":int}

class Objective(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    objective_text = Column(String(100), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    keyresult = relationship("Keyresult")

    def __repr__(self):
        return "<Objective(id='%s',objective_text='%s')>" % (
            self.id,
            self.objective_text
        )

    @classmethod
    def last_five_days_data(cls, session,start_time):
        return session.query(Objective).filter(Objective.created >= start_time).all()

    FIELDS = {"objective_text": str}

    FIELDS.update(Base.FIELDS)

class Keyresult(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(20), nullable=True)
    due_date = Column(DateTime)
    Objective_Id = Column(Integer, ForeignKey('objective.id'))

    def __repr__(self):
        return "<Keyresult(id='%s',status='%s',Objective_Id='%s')>" % (
            self.id,
            self.status,
            self.Objective_Id
        )

    FIELDS = {"status": str,"Objective_Id":int}

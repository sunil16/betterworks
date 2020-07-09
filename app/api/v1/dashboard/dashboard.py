import falcon
import datetime
import re
from sqlalchemy.sql import func
from sqlalchemy import or_

from app import log
from app.api.common import BaseResource
from app.errors import AppError
from app.model import *
from app.utils import find_day, get_delta_date_and_day

LOG = log.get_logger()

class Dashboard(BaseResource):
    """
    Handle for endpoint: /v1/dashboard/
    """

    GETOBJECTIVE = "objectives"
    GETALLDEPTNTEAM = "departments"

    def on_get(self, req, res):
        cmd = re.split("\\W+", req.path)[-1:][0]
        if cmd == self.GETOBJECTIVE:
            self.get_objectives(req, res)
        elif cmd == self.GETALLDEPTNTEAM:
            self.get_dept_and_team(req, res)

    def get_objectives(self, req, res):
        session = req.context["session"]

        day,start_date = get_delta_date_and_day(5)

        total_objectives = Objective.last_five_days_data(session, start_date)
        complete_objectives = session.query(Objective).join(Keyresult).filter(Objective.created >= start_date, Keyresult.status == 'Complete').all()

        if total_objectives is not None and complete_objectives is not None:
            obj = {"total_objectives":len(total_objectives), "complete_objectives": len(complete_objectives), "day_name": day}
            self.on_success(res, obj)
        else:
            raise AppError()

    def get_dept_and_team(self, req, res):
        session = req.context["session"]

        day,start_date = get_delta_date_and_day(5)
        dept_n_team = session.query(Department,Team,User,Objective,Keyresult).filter(Department.id == Team.department_id, Team.id==User.team_id,User.id==Objective.user_id,Objective.created >= start_date,Objective.id==Keyresult.Objective_Id)

        #getting department position in the db return array
        department_position = self.get_result(map(lambda d_model: d_model[0] if d_model[1].__tablename__ == 'department' else None, enumerate(dept_n_team[0]))) if dept_n_team.count() else None
        data = {}
        for info in dept_n_team:
            temp_data = {}
            department = info[department_position]
            p_obj,com_obj = self.get_objectives_details(info,'keyresult')
            emp = self.get_emp(info,'user')
            emp = emp if emp else {}
            obj = self.get_objectives(info,'objective')
            obj = obj if obj else {}
            if department.id in data.keys():
                temp_data = data[department.id]
                temp_data["pending_objectives"] = data[department.id]["pending_objectives"] + p_obj
                temp_data["complete_objectives"] = data[department.id]["complete_objectives"] + com_obj
                if emp.get('id') not in data[department.id]["employees"].keys():
                    temp_data["employees"].__setitem__(emp.get('id'),emp)
                if obj.get('id') not in data[department.id]["objectives"].keys():
                    temp_data["objectives"].__setitem__(obj.get('id'),obj)
                data[department.id] = temp_data
            else:
                temp_data['department_id'] = department.id
                temp_data['department_name'] = department.name
                temp_data["pending_objectives"] = p_obj
                temp_data["complete_objectives"] = com_obj
                temp_data["employees"] = { emp.get('id') : emp }
                temp_data["objectives"] = { obj.get('id') : obj }
                data[department.id] = temp_data

        if dept_n_team is not None:
            self.on_success(res, data)
        else:
            raise AppError()

    def get_result(self,data=None):
        if(data != None):
            result = None
            for itm in data:
                if itm != None:
                    result = itm
            return result
        return None

    def get_objectives(self,data=None,table_name=None):
        return self.get_result(map(lambda u_model: {"id" : u_model.id, "objective_text": u_model.objective_text } if u_model.__tablename__ == table_name else None, data))

    def get_emp(self,data=None,table_name=None):
        return self.get_result(map(lambda u_model: {"id" : u_model.id, "emp_name": u_model.first_Name } if u_model.__tablename__ == table_name else None, data))

    def get_objectives_details(self,data=None,table_name=None):
        return self.get_result(map(lambda kr_model: ((0,1) if kr_model.status == 'Complete' else (1,0)) if kr_model.__tablename__ == table_name else None, data))

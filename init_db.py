import json
import tqdm
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Client, Planner, Talent, JobManager, Base

try:
    os.remove('planning.db')
    print("Database already exists. It will be recreated...")
except OSError:
    pass

with open('planning.json') as json_file:
    data = json.load(json_file)

engine = create_engine('sqlite:///planning.db')

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

for item in tqdm.tqdm(data):
    id = item["id"]
    original_id = item["originalId"]
    talent_id = item["talentId"]
    talent_name = item["talentName"]
    talent_grade = item["talentGrade"]
    booking_grade = item["bookingGrade"]
    operating_unit = item["operatingUnit"]
    office_city = item["officeCity"]
    office_postal_code = item["officePostalCode"]
    job_manager_name = item["jobManagerName"]
    job_manager_id = item["jobManagerId"]
    total_hours = item["totalHours"]
    start_date_string = item["startDate"]
    end_date_string = item["endDate"]
    client_name = item["clientName"]
    client_id = item["clientId"]
    industry = item["industry"]
    is_unassigned = item["isUnassigned"]

    existing_client = session.query(Client).filter_by(id=client_id).first()
    existing_talent = session.query(Talent).filter_by(id=talent_id).first()
    existing_job_manager = session.query(JobManager).filter_by(id=job_manager_id).first()

    if existing_client:
        client = existing_client
    else:
        client = Client(id=client_id,
                        client_name=client_name,
                        industry=industry,
                        is_unassigned=is_unassigned)
        session.add(client)

    if existing_talent:
        talent = existing_talent
    else:
        talent = Talent(id=talent_id,
                        talent_name=talent_name,
                        talent_grade=talent_grade,
                        operating_unit=operating_unit,
                        office_city=office_city,
                        office_postal_code=office_postal_code)
        session.add(talent)

    if existing_job_manager:
        job_manager = existing_job_manager
    else:
        job_manager = JobManager(id=job_manager_id,
                   job_manager_name=job_manager_name)
        session.add(job_manager)

    start_date = datetime.strptime(start_date_string, "%m/%d/%Y %I:%M %p")
    end_date = datetime.strptime(end_date_string, "%m/%d/%Y %I:%M %p")

    planner = Planner(id=id,
                      original_id=original_id,
                      client_id=client_id,
                      talent_id=talent_id,
                      job_manager_id=job_manager_id,
                      total_hours=total_hours,
                      start_date=start_date,
                      end_date=end_date)
    session.add(planner)

session.commit()

session.close()

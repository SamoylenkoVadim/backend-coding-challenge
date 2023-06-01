from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Planner

engine = create_engine('sqlite:///planning.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
session = SessionLocal()

app = FastAPI()


@app.get("/planner")
def get_info(id: int):
    item = session.query(Planner).filter_by(id=id).first()
    data = {
        "id": item.id,
        "originalId": item.original_id,
        "talentId": item.talent.id,
        "talentName": item.talent.talent_name,
        "talentGrade": item.talent.talent_grade,
        "bookingGrade": item.talent.booking_grade,
        "operatingUnit": item.talent.operating_unit,
        "officeCity": item.talent.office_city,
        "officePostalCode": item.talent.office_postal_code,
        "jobManagerName": item.job_manager.job_manager_name,
        "jobManagerId": item.job_manager.id,
        "totalHours": item.total_hours,
        "startDate": item.start_date.strftime("%m/%d/%Y %I:%M %p"),
        "endDate": item.end_date.strftime("%m/%d/%Y %I:%M %p"),
        "clientName": item.client.client_name,
        "clientId": item.client.id,
        "industry": item.client.industry,
        "isUnassigned": item.client.is_unassigned,
        "requiredSkills": [],
        "optionalSkills": []
    }

    for association in item.planner_associations:
        skill_name = association.skill.skill_name
        skill_category = association.skill.skill_category
        skill = {
                "name": skill_name,
                "category": skill_category
            }
        if association.mandatory:
            data['requiredSkills'].append(skill)
        else:
            data['optionalSkills'].append(skill)

    return JSONResponse(content=data)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

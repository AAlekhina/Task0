import json
import os


from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@172.19.0.2:{os.getenv('PORT')}/{os.getenv('DATABASE_NAME')}"
def export_students_to_json():
    engine = create_engine(DATABASE_URL)
    SESSION = sessionmaker(bind=engine)
    session = SESSION()
    metadata = MetaData()
    students_table = Table('students', metadata,autoload_with=engine, schema = 'public')
    with engine.connect() as conn:
        results = conn.execute(students_table.select())
        data = []
        for i in results.fetchall():
            data.append({
                'id': i.id,
                'birthday': i.birthday,
                'name': i.name,
                'sex': i.sex,
                'room': i.room
            })
        with open('query_0.json', 'w') as f:
            json.dump(data, f, indent=4)
    session.close()
if __name__ == '__main__':
    export_students_to_json()


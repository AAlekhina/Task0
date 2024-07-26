import json
import os
from sqlalchemy import create_engine,Table, MetaData, func
from sqlalchemy.engine import row
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, join
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@172.19.0.2:{os.getenv('PORT')}/{os.getenv('DATABASE_NAME')}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()
metadata.bind = engine


rooms_table = Table('rooms', metadata, autoload_with = engine, schema = 'public')
students_table = Table('students', metadata, autoload_with = engine, schema = 'public')
query = (
    select(
        rooms_table.c.name.label('room'),
        func.count(students_table.c.id).label('number_of_students')
    )
    .select_from(
        join(rooms_table, students_table, rooms_table.c.id == students_table.c.room)
    )
    .group_by(rooms_table.c.name)
    .order_by(func.count(students_table.c.id).desc())
)

results = session.execute(query).fetchall()
data = [
    {
        "room": row.room,
        "number_of_students": row.number_of_students
    }
    for row in results
]
with open('query_count.json', 'w') as f:
    json.dump(data, f, indent = 4)
print("sucsesfull write query count")
session.close()


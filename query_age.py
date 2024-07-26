import json
import os
from sqlalchemy import create_engine, Table, MetaData, func, cast, Date, extract
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, join
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Construct DATABASE_URL
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@172.19.0.2:{os.getenv('PORT')}/{os.getenv('DATABASE_NAME')}"

# Initialize the database engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Reflect the existing database schema
metadata = MetaData()
metadata.bind = engine

rooms_table = Table('rooms', metadata, autoload_with=engine, schema='public')
students_table = Table('students', metadata, autoload_with=engine, schema='public')

# Calculate the age in years
age_years = extract('year', func.age(cast(students_table.c.birthday, Date))).label('age')

# Construct the query
query = (
    select(
        func.json_build_object(
            'room', rooms_table.c.name,
            'avg_age', func.avg(age_years)
        ).label('student_avg')
    )
    .select_from(
        join(rooms_table, students_table, rooms_table.c.id == students_table.c.room)
    )
    .group_by(rooms_table.c.name)
    .order_by(func.avg(age_years))
    .limit(5)
)

# Execute the query
result = session.execute(query).fetchall()

# Prepare data for JSON
data = [row.student_avg for row in result]

# Write data to JSON file
output_file = "rooms_average_age.json"
with open(output_file, 'w') as f:
    json.dump(data, f, indent=4)

# Print the path to the JSON file
print(f"Data has been written to {output_file}")

# Close the session
session.close()
import json
import os
from sqlalchemy import create_engine, Table, MetaData, func
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

query = (
    select(
            rooms_table.c.name.label('room_name')
        )
        .select_from(
            join(rooms_table, students_table, rooms_table.c.id == students_table.c.room)
        )
        .group_by(rooms_table.c.name)
        .having(func.count(func.distinct(students_table.c.sex)) > 1)
)


# Execute the query
result = session.execute(query).fetchall()

# Prepare data for JSON
data = [row.room_name for row in result]

# Write data to JSON file
output_file = "rooms_gender.json"
with open(output_file, 'w') as f:
    json.dump(data, f, indent=4)

# Print the path to the JSON file
print(f"Data has been written to {output_file}")

# Close the session
session.close()
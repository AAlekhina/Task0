import json
import os
from sqlalchemy import create_engine, Table, MetaData, func, cast, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from sqlalchemy.orm import aliased
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@172.19.0.2:{os.getenv('PORT')}/{os.getenv('DATABASE_NAME')}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()
metadata.bind = engine

students_table = Table('students', metadata, autoload_with = engine, schema='public')
s2 = aliased(students_table)

subquery = (
    select(
        s2.c.room,
        func.max(cast(s2.c.birthday, Date)).over(partition_by=s2.c.room).label('max_date'),
        func.min(cast(s2.c.birthday, Date)).over(partition_by=s2.c.room).label('min_date')
    ).alias('s2')
)


query = (
    select(
        subquery.c.room,
        (func.extract('year', func.age(cast(subquery.c.max_date, Date), cast(subquery.c.min_date, Date)))).label('age_diff')
    )
    .group_by(subquery.c.room, func.extract('year', func.age(cast(subquery.c.max_date, Date), cast(subquery.c.min_date, Date))))
    .order_by(func.extract('year', func.age(cast(subquery.c.max_date, Date), cast(subquery.c.min_date, Date))).desc())
    .limit(5)
)

result = session.execute(query).fetchall()
data = [{'room': row.room, 'age_diff': str(row.age_diff)} for row in result]
with open('query_age_diff.json', 'w') as f:
    json.dump(data, f, indent = 4)
print('succsesfully')
session.close()

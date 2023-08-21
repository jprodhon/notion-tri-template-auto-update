import os
from notion_api_functions import *
from your_db_id import *

from notion_client import Client
os.environ['NOTION_TOKEN'] = notion_token
notion = Client(auth=os.environ["NOTION_TOKEN"])

db1 = notion.databases.query(database_id = db1_id)

first_year, first_week, last_year, last_week = date_limits(db1)

nb_max = 12*(last_year-first_year) + last_week-first_week + 1

db2 = notion.databases.query(database_id = db2_id)
update_db2(notion, db2, db2_id, nb_max, sport_list_ext)

db2 = notion.databases.query(database_id = db2_id)
week_db2 = get_db2(db2, sport_list_ext)

update_db1(notion, db1, week_db2, sport_list, first_year, first_week)
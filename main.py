import os
from notion_api_functions import *
from your_db_id import *

if len(calendar_db_id) != 32:
    raise ValueError("calendar database id length should be equal to 32")
if len(week_db_id) != 32:
    raise ValueError("week database id length should be equal to 32")

from notion_client import Client
os.environ['NOTION_TOKEN'] = notion_token
notion = Client(auth=os.environ["NOTION_TOKEN"])

calendar_db = notion.databases.query(database_id = calendar_db_id)

first_year, first_week, last_year, last_week = date_limits(calendar_db)

nb_max = 12*(last_year-first_year) + last_week-first_week + 1

week_db = notion.databases.query(database_id = week_db_id)
update_week_db(notion, week_db, week_db_id, nb_max, sport_list_ext)

week_db = notion.databases.query(database_id = week_db_id)
week_all_db = get_week_db(week_db, sport_list_ext)

update_calendar_db(notion, calendar_db, week_all_db, sport_list, first_year, first_week)
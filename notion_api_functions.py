import datetime

def sport_json(sport):
    if sport == "Swim":
        chain = {'id': 'nn%3Ff',
                 'select': {'color': 'blue',
                            'id': 'Qcf|',
                            'name': 'Swim'},
                 'type': 'select'}
    elif sport == "Bike":
        chain = {'id': 'nn%3Ff',
                 'select': {'color': 'brown',
                            'id': '@WW:',
                            'name': 'Bike'},
                 'type': 'select'}
    elif sport == "Run":
        chain = {'id': 'nn%3Ff',
                 'select': {'color': 'green',
                            'id': 'bMRh',
                            'name': 'Run'},
                 'type': 'select'}
    elif sport == "All":
        chain = {'id': 'nn%3Ff',
                 'select': {'color': 'default',
                            'id': 'gly:',
                            'name': 'All'},
                 'type': 'select'}
    else: chain = ""
    return chain

def get_date(date):
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])
    week = datetime.date(year, month, day).isocalendar().week
    return week, year

def date_limits(db1):
    first_week = 100
    first_year = 3000
    last_week = 0
    last_year = 1000
    for workout in db1["results"]:
        date = workout["properties"]["Date"]["date"]["start"]
        week, year = get_date(date)
        if year < first_year or (year == first_year and week < first_week):
            first_year = year
            first_week = week
        if year > last_year or (year == last_year and week > last_week):
            last_year = year
            last_week = week
    return first_year, first_week, last_year, last_week


def update_db2(notion, db2, db2_id, nb_max, sport_list):
    for sport in sport_list:
        week_list = []
        for week in db2["results"]:
            wk = int(week["properties"]["Week"]["title"][0]["plain_text"])
            wk_sport = week["properties"]["Sport"]["select"]["name"]
            if wk_sport == sport:
                if wk < 1 or wk > nb_max:
                    notion.pages.update(page_id = week["id"], archived = True)
                else:
                    week_list.append(wk)
        for wk in range(1,nb_max+1):
            if wk not in week_list:
                new_page = { 'Week': {'title': [{'text': {'content': str(wk)}}]}, 
                             'Sport': sport_json(sport),
                           }
                notion.pages.create(parent={"database_id": db2_id}, properties=new_page)

def get_db2(db2, sport_list):
    week_l = {}
    for sport in sport_list:
        week_l[sport] = {}
    for week in db2["results"]:
        wk = int(week["properties"]["Week"]["title"][0]["plain_text"])
        sport = week["properties"]["Sport"]["select"]["name"]
        week_l[sport][wk] = week["id"]
    return week_l

def update_db1(notion, db1, week_list, sport_list, first_year, first_week):
    for workout in db1["results"]:
        sport = workout["properties"]["Sport"]["select"]["name"]
        if workout["properties"]["Sport"]["select"]["name"] == sport:
            date = workout["properties"]["Date"]["date"]["start"]
            week, year = get_date(date)
            nb = 12*(year - first_year) + (week - first_week) + 1
            prop = {'Week link': {'relation': [{'id': week_list[sport][nb]},{'id': week_list["All"][nb]}],
                                   'type': 'relation'} }
            notion.pages.update(page_id = workout["id"], properties = prop)
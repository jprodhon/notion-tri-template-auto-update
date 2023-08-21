# Auto-sync Notion training template

First you need to create a new integration on your Notion account for Python
[Notion integration](https://www.notion.so/my-integrations)

Save the secret key generated and put it in your_db_id.py file in the notion_token variable
Open the Notion template page, copy the page id, the calendar database id and the week database id. These id are 32 characters long. Put these id in the your_db_id.py file in the variables associated.

Then
```python
pip install notion-client
```

and finally:
```python
python main.py
```

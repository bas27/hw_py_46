import json
import datetime
import requests, time

def stack_quest(number_days):
    
    questions = []
    today = datetime.date.today()
    last_day = today - datetime.timedelta(days=number_days)
    i = 0

    while True:
        
        URL = 'https://api.stackexchange.com/2.3/questions'
        page = str(i + 1)
        params = {
            'tagged': 'python',
            'site': 'stackoverflow.com',
            'fromdate': str(last_day),
            'todate': str(today),
            'order': 'desc',
            'sort': 'activity',
            'pagesize': '100',
            'page': page
        }
        response = requests.get(URL, params=params)
        data = json.loads(response.text)
        
        for item in data['items']:
            questions.append(item)
        
        # print("Processed page " + str(i + 1) + ", returned " + str(response))
        time.sleep(2) # timeout not to be rate-limited
        
        if response.json()['has_more'] != True:
            break
        
        i += 1

    for i, q in enumerate(questions, start=1):
        print(f"{i}. {q['title']}")

stack_quest(1)
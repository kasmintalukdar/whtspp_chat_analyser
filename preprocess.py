import regex as re
import pandas as pd
from datetime import datetime

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    massage = re.split(pattern, data)[4:]
    dates = re.findall(pattern, data)[3:]
    df = pd.DataFrame({'date': dates, "massages": massage})
    df['date'] = df['date'].apply(lambda t: datetime.strptime(t, '%d/%m/%y, %H:%M - '))
    users = []
    user_messages = []
    for message in df['massages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            user_messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            user_messages.append(entry[0])
    df['users'] = users
    df['massages'] = user_messages
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] =period


    return df
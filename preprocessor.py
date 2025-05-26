import re
import pandas as pd

def preprocess(data):

    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'


    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)


    df = pd.DataFrame({'message_date': dates, 'user_message': messages})


    df['clean_date'] = df['message_date'].str.extract(r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2})')

    df['message_data'] = pd.to_datetime(df['clean_date'], format='%d/%m/%y, %H:%M', errors='coerce')

    df.rename(columns={'message_date': 'raw_date'}, inplace=True)


    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if len(entry) > 2:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages


    df.drop(columns=['user_message', 'raw_date', 'clean_date'], inplace=True)


    df['year'] = df['message_data'].dt.year
    df['month_num']=df['message_data'].dt.month
    df['month'] = df['message_data'].dt.month_name()
    df['day'] = df['message_data'].dt.day
    df['hour'] = df['message_data'].dt.hour
    df['minute'] = df['message_data'].dt.minute

    return df




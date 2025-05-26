# def fetch_stats(selected_user,df):
#
#     if selected_user=='Overall':
#         num_messages=df.shape[0]
#
#         words=[]
#         for mess in df['message']:
#             words.extend(mess.split())
#
#         return num_messages,len(words)
#
#     else:
#         new_df = df[df['user'] == selected_user]
#         num_messages = new_df.shape[0]
#
#         words = []
#         for mess in new_df['message']:
#             words.extend(mess.split())
#
#         return num_messages,len(words)
#
import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
extract=URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())

    # Use the correct string depending on your file
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages,len(links)

def most_busy_user(df):
    x = df['user'].value_counts().head()

    percent_df = round(df['user'].value_counts() / df.shape[0] * 100, 2).reset_index()
    percent_df.columns = ['user', 'percent']

    return x, percent_df


def create_wordcloud(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=""))
    return df_wc

def most_common_words(selected_user,df):

    f=open('stop_hinglish.txt','r')
    stop_words=f.read()

    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']

    words=[]

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)


    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    emojis=[]
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    return len(emojis)


def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]


    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()


    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline







from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import emoji
import regex as re
import pandas as pd
def analyse(df,user):
    if user!='Overall':
        df = df[df['users'] == user]
    #count of massages
    total_massage=df[df['users']!='group_notification']['massages'].shape[0]
    #count of words
    words = []
    for massage in df['massages']:
        words.extend(massage.split(' '))
    word_count=len(words)
    #media massage
    media_massage=df[df['massages'] == '<Media omitted>\n'].shape[0]
    #urls
    extractor = URLExtract()
    links = []
    for message in df['massages']:
        links.extend(extractor.find_urls(message))
    link_count=len(links)

    return total_massage,word_count,media_massage,link_count
#most busy user
def busy(df):
    top_user_df = pd.DataFrame(df[df['users'] != 'group_notification']['users'].value_counts()).reset_index().rename(
        columns={'index': "Users", "users": "message_in_percentage"})
    top_user_df["message_in_percentage"] = round(((top_user_df["message_in_percentage"] / len(df)) * 100), 2)
    return top_user_df
#bar plot
def bar_ploter(x,y,rotation,xlabel,ylabel,c='purple'):
    fig, ax = plt.subplots()
    ax.bar(x, y, color=c)
    plt.xticks(rotation=rotation);
    plt.xlabel(xlabel)
    plt.ylabel(ylabel);
    return fig
#word cloud
def wordcloud(df,user):
    if user != 'Overall':
        df = df[df['users'] == user]
    f = open('hindistopword.txt', 'r')
    stop_words = f.read()
    stop_words_split = stop_words.split('\n')
    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['massages'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words_split:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=300, height=300, min_font_size=10, background_color='white')
    temp['massages'] = temp['massages'].apply(remove_stop_words)
    df_wc = wc.generate(temp['massages'].str.cat(sep=" "))
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    return fig
#most common word
def most_common_words(df,user):
    if user != 'Overall':
        df = df[df['users'] == user]
    f = open('hindistopword.txt', 'r')
    stop_words = f.read()

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['massages'] != '<Media omitted>\n']

    words = []

    for message in temp['massages']:
        res = re.sub(r'[^\w\s]', '', message)
        for word in res.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20)).rename(columns={0:"words",1:"count"})
    return most_common_df
#most used emoji
def emoji_helper(df,user):
    if user != 'Overall':
        df = df[df['users'] == user]
    emojis = []
    for message in df['massages']:
        emojis.extend([c for c in message if c in emoji.distinct_emoji_list(message)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis)))).rename(columns={0: 'emoji', 1: 'counts'})

    return emoji_df
#monthly timeline
def monthly_timeline(df,user):
    if user != 'Overall':
        df = df[df['users'] == user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['massages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline
#Daily timeline
def daily_timeline(df,user):
    if user != 'Overall':
        df = df[df['users'] == user]

    daily_timeline = df.groupby('only_date').count()['massages'].reset_index()

    return daily_timeline
#weakly activity map
def week_activity_map(df,user):
    if user != 'Overall':
        df = df[df['users'] == user]
    return df['day_name'].value_counts()
#monthly ctivity map
def month_activity_map(df,user):
    if user != 'Overall':
        df = df[df['users'] == user]
    return df['month'].value_counts()
#Activity heatmap
def activity_heatmap(df,user):
    if user != 'Overall':
        df = df[df['users'] == user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='massages', aggfunc='count').fillna(0)

    return user_heatmap


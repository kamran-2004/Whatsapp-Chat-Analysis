from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extractor = URLExtract()

def fetch_stats(selected_user,df):


    if selected_user != 'Overall':
        df = df[df['user'] ==selected_user]
    #Fetching number of messages 

    num_messages = df.shape[0]

    #Number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    #fetch number of medias
    num_media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]   

    #Fetch Number of Links
    links=  []

    for message in df['message']:
     links.extend(extractor.find_urls(message))
    


    return num_messages,words, num_media_msg,links
    
    
def feth_most_busy_users(df):
   x = df['user'].value_counts().head()
   df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns = {'index':'name', 'user':'percent'})
   return x ,df;

def create_word_cloud(selected_user,df):
   
   if selected_user != 'Overall':
    df = df[df['user'] ==selected_user]
   temp = df[df['user'] != 'group_notification']  
   temp = temp[temp['message'] != '<Media omitted>\n']
   f = open('stop_hinglish.txt','r')
   stop_words = f.read() 
   def remove_stop_words(message):
      y = []
      for word in message.lower().split():
         if word not in stop_words:
            y.append(word)

      return " ".join(y)      
      
   wc = WordCloud(width = 500, height = 500, min_font_size= 10, background_color = 'white')

   temp['message'] = temp['message'].apply(remove_stop_words)

   df_wc = wc.generate(temp['message'].str.cat(sep=  " "))
   return df_wc
   
def most_common_words(selected_user,df):
   if selected_user != 'Overall':
    df = df[df['user'] ==selected_user]
   temp = df[df['user'] != 'group_notification']  
   temp = temp[temp['message'] != '<Media omitted>\n']
   f = open('stop_hinglish.txt','r')
   stop_words = f.read()
   words= []
   for message in temp['message']:
    for word in message.lower().split():
        if word not in stop_words:
         words.append(word)
   most_common_df =   pd.DataFrame(Counter(words).most_common(20))    
   return  most_common_df ; 

def emoji_helper(selected_user, df):
   if selected_user != 'Overall':
    df = df[df['user'] ==selected_user]

   def extract_emojis(message):
    return [char for char in message if emoji.is_emoji(char)]
   
   emojis = []
   for message in df['message']:
    emojis.extend(extract_emojis(message))

   emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
   return emoji_df 

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap



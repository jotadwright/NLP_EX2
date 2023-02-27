import pandas as pd

# Load and clean the search results from CSV
df_info = pd.read_csv('data/info_nouns.csv',names=['noun','info_freq'])
df_event = pd.read_csv('data/event_nouns.csv',names=['noun','event_freq'])
df_info = df_info.drop([0])
df_event = df_event.drop([0])
df_info = df_info.sort_values(by='info_freq',ascending=False)
df_event = df_event.sort_values(by='event_freq',ascending=False)

df_info.to_csv('data/info_nouns.csv', index=False)
df_event.to_csv('data/event_nouns.csv', index=False)

# Get the intersection of the two sets of results and save to CSV
shared = set(df_info['noun']).intersection(df_event['noun'])
df_info = df_info[df_info['noun'].isin(shared)]
df_event = df_event[df_event['noun'].isin(shared)]

df = pd.merge(df_info,df_event,how='inner')

df.to_csv('data/merge.csv', index=False)

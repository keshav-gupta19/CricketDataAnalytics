import json
import pandas as pd

with open('datasets/json/t20_wc_match_results.json') as f:
    data = json.load(f)

df_match = pd.DataFrame(data[0]['matchSummary'])
df_match.rename({'scorecard': 'match_id'}, axis=1, inplace=True)
match_ids_dict={}
for index,row in df_match.iterrows():
    key1 = row['team1']+' Vs '+row['team2']
    key2 = row['team2'] + ' Vs ' + row['team1']
    match_ids_dict[key1]=row["match_id"]
    match_ids_dict[key2] = row["match_id"]
# print(match_ids_dict)
with open('datasets/json/t20_wc_batting_summary.json') as f:
    data=json.load(f)
    all_record=[]
    for rec in data:
        all_record.extend(rec['battingSummary'])
df_batting=pd.DataFrame(all_record)
df_batting["out/not_out"]=df_batting.dismissal.apply(lambda x: "out" if len(x)>0 else "not_out")
df_batting.drop(columns=["dismissal"], inplace=True)
df_batting['batsmanName'] = df_batting['batsmanName'].apply(lambda x: x.replace('â€', ''))
df_batting['batsmanName'] = df_batting['batsmanName'].apply(lambda x: x.replace('\xa0', ''))
df_batting['match_id']= df_batting["match"].map(match_ids_dict)
# print(df_batting.head())
df_batting.to_csv('datasets/csv/fact_batting_summary.csv', index=False)

with open('jsonfiles/t20_wc_bowling_summary.json') as f:
    data = json.load(f)
    all_records = []
    for rec in data:
        all_records.extend(rec['bowlingSummary'])
# all_records[:2]
df_bowling = pd.DataFrame(all_records)
df_bowling['match_id'] = df_bowling['match'].map(match_ids_dict)
df_bowling.to_csv('jsonfiles/fact_bowling_summary.csv', index = False)

with open('jsonfiles/t20_wc_player_info.json') as f:
    data = json.load(f)
df_players = pd.DataFrame(data)
df_players['name'] = df_players['name'].apply(lambda x: x.replace('â€', ''))
df_players['name'] = df_players['name'].apply(lambda x: x.replace('†', ''))
df_players['name'] = df_players['name'].apply(lambda x: x.replace('\xa0', ''))
df_players.to_csv('t20_csv_files/dim_players_no_images.csv', index = False)

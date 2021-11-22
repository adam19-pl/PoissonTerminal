import http.client
import json
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import math
import datetime

# Ustalenie zakresu czasowego od kiedy do kiedy będą brane dane
actuall_date = datetime.datetime.today()
time_range = actuall_date - datetime.timedelta(weeks=6)
time_range = time_range.strftime('%Y-%m-%d')

footbal_team = input("Wpisz nazwę druzyny którą chcesz sprawdzić : ")
footbal_team_read = footbal_team.replace(" ", "%20")

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "Your API KEY"
}


##### Pobieranie wszystkich lig

conn.request("GET", "/leagues", headers=headers)

res = conn.getresponse()
data = res.read()
datajson = json.loads(data.decode('utf-8'))

file_location = "all_leagues.json"
with open(file_location, 'w') as f:
    json.dump(datajson, f, indent=4)

###
conn.request("GET", "/teams", headers=headers)

res = conn.getresponse()
data = res.read()
datajson = json.loads(data.decode('utf-8'))

file_location = "all_teams.json"
with open(file_location, 'w') as f:
    json.dump(datajson, f, indent=4)
#####

conn.request("GET", f"/teams?name={footbal_team_read}", headers=headers)

res = conn.getresponse()
data = res.read()
datajson = json.loads(data.decode('utf-8'))

file_location = "data_first_team.json"
with open(file_location, 'w') as f:
    json.dump(datajson, f, indent=4)


footbal_team_info = datajson['response']
footbal_team_first_id = datajson['response'][0]['team']['id']
footbal_team_first_country = datajson['response'][0]['team']['country']

footbal_team2 = input("Wpisz nazwę drugiej druzyny którą chcesz sprawdzić : ")
footbal_team_read2 = footbal_team2.replace(" ", "%20")

conn.request("GET", f"/teams?name={footbal_team_read2}", headers=headers)
res = conn.getresponse()
data = res.read()
datajson_second_team = json.loads(data.decode('utf-8'))
file_location = "data_second_team.json"
with open(file_location, 'w') as f:
    json.dump(datajson_second_team, f, indent=4)

footbal_team_second_id = datajson_second_team['response'][0]['team']['id']
footbal_team_second_country = datajson_second_team['response'][0]['team']['country']


conn.request("GET", f"/leagues?team={footbal_team_first_id}", headers=headers)

res = conn.getresponse()
data = res.read()
datajson = json.loads(data.decode('utf-8'))

file_location = "datapr.json"
with open(file_location, 'w') as f:
    json.dump(datajson, f, indent=4)

footbal_team_info_league = datajson['response'][0]['league']['id']
football_season = 2021

conn.request("GET", f"/leagues?team={footbal_team_second_id}", headers=headers)

res = conn.getresponse()
data = res.read()
datajson_second_team_league = json.loads(data.decode('utf-8'))

file_location = "data_second_team_league.json"
with open(file_location, 'w') as f:
    json.dump(datajson_second_team_league, f, indent=4)

footbal_team_second_info_league = datajson_second_team_league['response'][0]['league']['id']
football_season = 2021

## Pobieranie danych do dnia aktualnego
conn.request("GET",
             f"/teams/statistics?season={football_season}&team={footbal_team_first_id}&league={footbal_team_info_league}",
             headers=headers)

res = conn.getresponse()
data = res.read()
datajson_first_team_statistic_actual_date = json.loads(data.decode('utf-8'))

file_location = "data_first_team_statistics_actual_date.json"
with open(file_location, 'w') as f:
    json.dump(datajson_first_team_statistic_actual_date, f, indent=4)



## musisz utworzyć jeszcze jeden request dotyczący statystyk drugiej druzyny i zapisać go do pliku :)_
#parametr date oznacza do kiedy ma pobierać dane
conn.request("GET",
             f"/teams/statistics?season={football_season}&team={footbal_team_first_id}&league={footbal_team_info_league}&date={time_range}",
             headers=headers)

res = conn.getresponse()
data = res.read()
datajson_first_team_statistic = json.loads(data.decode('utf-8'))

file_location = "data_first_team_statistics.json"
with open(file_location, 'w') as f:
    json.dump(datajson_first_team_statistic, f, indent=4)

# druga drużyna pobieranie danych do dnia dzisiejszego
conn.request("GET",
             f"/teams/statistics?season={football_season}&team={footbal_team_second_id}&league={footbal_team_second_info_league}",
             headers=headers)

res = conn.getresponse()
data = res.read()
datajson_second_team_statistic_actual_date = json.loads(data.decode('utf-8'))

file_location = "data_second_team_statistics_actual_date.json"
with open(file_location, 'w') as f:
    json.dump(datajson_second_team_statistic_actual_date, f, indent=4)


# druga drużyna pobieranie danych z zakresu -6tygodni od aktualnej daty
conn.request("GET",
             f"/teams/statistics?season={football_season}&team={footbal_team_second_id}&league={footbal_team_second_info_league}&date={time_range}",
             headers=headers)

res = conn.getresponse()
data = res.read()
datajson_second_team_statistic = json.loads(data.decode('utf-8'))

file_location = "data_second_team_statistics.json"
with open(file_location, 'w') as f:
    json.dump(datajson_second_team_statistic, f, indent=4)


#footbal_team_second_statistics_form = datajson_second_team_statistic['response']['form']

conn.request("GET", f"/fixtures/headtohead?h2h={footbal_team_first_id}-{footbal_team_second_id}", headers=headers)

res = conn.getresponse()
data = res.read()
datajson5 = json.loads(data.decode('utf-8'))

file_location = "datah2h.json"
with open(file_location, 'w') as f:
    json.dump(datajson5, f, indent=4)

#pobranie formy druzyny :)

# Dane do dnia aktualnego
#Pierwsza drużyna
footbal_team_first_statistics_goal_total_actual_date = datajson_first_team_statistic_actual_date['response']['goals']['for']['total']['total'] # 47
footbal_team_first_statistics_played_match_total_actual_date = datajson_first_team_statistic_actual_date['response']['fixtures']['played']['total']
footbal_team_first_statistics_form = datajson_first_team_statistic['response']['form']
#Druga Druzyna
footbal_team_second_statistics_goal_total_actual_date = datajson_second_team_statistic_actual_date['response']['goals']['for']['total']['total']
footbal_team_second_statistics_played_match_total_actual_date = datajson_second_team_statistic_actual_date['response']['fixtures']['played']['total']

#Dane z zakresu od dnia aktualnego - 6 tygodni wstecz
footbal_team_first_statistics_goal_total = datajson_first_team_statistic['response']['goals']['for']['total']['total']
footbal_team_first_statistics_played_match_total = datajson_first_team_statistic['response']['fixtures']['played']['total']
footbal_team_second_statistics_goal_total = datajson_second_team_statistic['response']['goals']['for']['total']['total']
footbal_team_second_statistics_played_match_total = datajson_second_team_statistic['response']['fixtures']['played']['total']

# podsumowanie bramek z 6 tygodni
footbal_team_first_statistics_all_goal_6_weeks = footbal_team_first_statistics_goal_total_actual_date - footbal_team_first_statistics_goal_total
footbal_team_second_statistics_all_goal_6_weeks = footbal_team_second_statistics_goal_total_actual_date - footbal_team_second_statistics_goal_total
footbal_team_first_statistic_all_played_match_6_weeks = footbal_team_first_statistics_played_match_total_actual_date - footbal_team_first_statistics_played_match_total
footbal_team_second_statistic_all_played_match_6_weeks = footbal_team_second_statistics_played_match_total_actual_date - footbal_team_second_statistics_played_match_total


print(footbal_team_first_statistics_all_goal_6_weeks)
print(footbal_team_first_statistics_played_match_total)
## Obliczanie średniej
footbal_team_first_statistics_avarage_total = footbal_team_first_statistics_goal_total / footbal_team_first_statistics_played_match_total
footbal_team_second_statistics_avarage_total = footbal_team_second_statistics_goal_total / footbal_team_second_statistics_played_match_total

footbal_team_first_statistics_avarage_total_6_weeks = footbal_team_first_statistics_all_goal_6_weeks / footbal_team_first_statistic_all_played_match_6_weeks
footbal_team_second_statistics_avarage_total_6_weeks = footbal_team_second_statistics_all_goal_6_weeks / footbal_team_second_statistic_all_played_match_6_weeks

print(footbal_team_second_statistics_avarage_total)
k_elements = [0,1,2,3,4]
e_value = 2.718
poisson_result_second_team = []
poisson_result_first_team = []
poisson_result_first_team_6_weeks = []
poisson_result_second_team_6_weeks = []
for k_element in k_elements:
    poisson_summary_first_team = ((pow(footbal_team_first_statistics_avarage_total, k_element) * pow(e_value,-footbal_team_first_statistics_avarage_total))/math.factorial(k_element))*100
    poisson_result_first_team.append(poisson_summary_first_team)

    poisson_summary_second_team = ((pow(footbal_team_second_statistics_avarage_total, k_element) * pow(e_value,-footbal_team_second_statistics_avarage_total))/math.factorial(k_element))*100
    poisson_result_second_team.append(poisson_summary_second_team)

    poisson_summary_first_team_6_weeks = ((pow(footbal_team_first_statistics_avarage_total_6_weeks, k_element) * pow(e_value,-footbal_team_first_statistics_avarage_total_6_weeks))/math.factorial(k_element)) *100
    poisson_result_first_team_6_weeks.append(poisson_summary_first_team_6_weeks)

    poisson_summary_second_team_6_weeks = ((pow(footbal_team_second_statistics_avarage_total_6_weeks, k_element) * pow(e_value,-footbal_team_second_statistics_avarage_total_6_weeks))/math.factorial(k_element)) * 100
    poisson_result_second_team_6_weeks.append(poisson_summary_second_team_6_weeks)


print(f"Rozkład Poissona cały sezon/{footbal_team_second_statistics_played_match_total} meczy - {footbal_team2} Ilość goli  :")
print(poisson_result_second_team)
print(f"Rozkład Poissona cały sezon/{footbal_team_first_statistics_played_match_total} meczy - {footbal_team}  Ilość goli  :")
print(poisson_result_first_team)
print(f"Rozkład Poissona z ostatnich 6 tygodni / {footbal_team_second_statistic_all_played_match_6_weeks} meczy - {footbal_team2} Ilość goli  :")
print(poisson_result_second_team_6_weeks)
print(f"Rozkład Poissona z ostatnich 6 tygodni / {footbal_team_first_statistic_all_played_match_6_weeks} meczy - {footbal_team} Ilość goli  :")
print(poisson_result_first_team_6_weeks)
print(30*'-')
print(time_range)
print(footbal_team_first_statistics_all_goal_6_weeks)
print(footbal_team_first_statistic_all_played_match_6_weeks)
print(footbal_team_first_statistics_avarage_total_6_weeks)
print(footbal_team_second_statistics_all_goal_6_weeks)
print(footbal_team_second_statistic_all_played_match_6_weeks)
print(footbal_team_second_statistics_avarage_total_6_weeks)


# wstępne pokazanie wyników wykres do poprawy lub zamień na inny :)
fig = make_subplots(rows=1, cols=2, shared_yaxes=True)

fig.add_trace(go.Bar(x=[0, 1, 2, 3, 4], y=[x for x in poisson_result_first_team_6_weeks],
                    marker=dict(color=[4, 5, 6], coloraxis="coloraxis")),
              1, 1)

fig.add_trace(go.Bar(x=[0, 1, 2, 3, 4], y=[x for x in poisson_result_second_team_6_weeks],
                    marker=dict(color=[2, 3, 5], coloraxis="coloraxis")),
              1, 2)

fig.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=False)
fig.show()
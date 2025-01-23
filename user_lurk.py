#Imports
import cfbd, os, csv, subprocess

#Functions
def get_usage(player, curr):
    name = player.name

    overall = round(player.usage.overall * 100, 2)
    first_down = round(player.usage.first_down * 100, 2)
    second_down = round(player.usage.second_down * 100, 2)
    third_down = round(player.usage.third_down * 100, 2)

    player_data = api.player_search(search_term = name, team = curr)

    number = player_data[0].jersey

    if number == None:
        number = 0

    position = player_data[0].position

    if (position != 'QB'):
        data.append(['#' + str(number), name, position, str(overall) + '%', 
                     str(first_down) + '%', str(second_down) + '%',
                     str(third_down) + '%'])

#Variables
CFBD_API_KEY = 'YOUR API KEY HERE'
config = cfbd.Configuration()
config.api_key['Authorization'] = CFBD_API_KEY
config.api_key_prefix['Authorization'] = 'Bearer'

api = cfbd.PlayersApi(cfbd.ApiClient(config))
games_api = cfbd.GamesApi(cfbd.ApiClient(config))
title = 'User Lurk: Scouting System'

#To execute
os.system('cls')
print(title + '\n' + '-' * len(title))

#Get user info
team = input('Team: ')
year = int(input('Year: '))

#Create folder
folder_path = (r"YOUR PATH HERE" + 
               team.replace(' ', '_') + "_" + str(year))
os.mkdir(folder_path)

#Get the team schedule
schedule = games_api.get_games(year = year, team = team)


#Gather usage data
print('Gathering usage data (this could take a while)...\n')
for game in schedule:
    curr = ''
    data = [
        ['Number', 'Name', 'Position', 'Overall', 'First Down', 
         'Second Down', 'Third Down']
    ]

    if game.home_team == team:
        curr = game.away_team
    else:
        curr = game.home_team
    
    usage_data = api.get_player_usage(year = year, team = curr)
    usage_data.sort(key = lambda x: x.usage.overall, reverse = True)

    for player in usage_data:
        get_usage(player, curr)

    csv_path = folder_path + r"\\" + curr.replace(' ', '_') + '.csv'

    #Write usage data to a csv file
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    
    print('Data gathered for ' + curr)

print('\nAll data gathered')
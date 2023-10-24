import csv
import pybaseball
import player_data

teams = ["ANA", "ARI", "ATL", "BAL", "BOS", "CHA", "CHN", "CIN", "CLE", "COL", "DET", "HOU", "KCA", "LAN", "MIA", "MIL", "MIN", "NYA", "NYN", "OAK", "PHI", "PIT", "SDN", "SEA", "SFN", "SLN", "TBA", "TEX", "TOR", "WAS"]

#                  # None,    1,       2,       1&2,     3,       1&3,     2&3,     1&2&3
# scoring_probs = [[0.49583, 0.87301, 1.12041, 1.50710, 1.35678, 1.75823, 1.98880, 2.32324],
#                  [0.26307, 0.52016, 0.68950, 0.93060, 0.95275, 1.18038, 1.40224, 1.56560],
#                  [0.09897, 0.22080, 0.33137, 0.44388, 0.38050, 0.51086, 0.60300, 0.76776]]

# #2022           # None, 1,    2,    1&2,  3,    1&3,  2&3,  1&2&3
# scoring_probs = [[0.49, 0.90, 1.13, 1.49, 1.24, 1.78, 2.05, 2.47],
#                  [0.26, 0.53, 0.70, 0.94, 1.01, 1.20, 1.43, 1.58],
#                  [0.10, 0.21, 0.32, 0.45, 0.41, 0.52, 0.57, 0.80]]
# #2021           # None, 1,    2,    1&2,  3,    1&3,  2&3,  1&2&3
# scoring_probs = [[0.52, 0.94, 1.17, 1.56, 1.46, 1.79, 2.16, 2.50],
#                  [0.27, 0.55, 0.71, 0.94, 0.98, 1.16, 1.42, 1.71],
#                  [0.10, 0.23, 0.33, 0.46, 0.39, 0.50, 0.61, 0.83]]
# #2020           # None, 1,    2,    1&2,  3,    1&3,  2&3,  1&2&3
# scoring_probs = [[0.53, 0.93, 1.18, 1.63, 1.45, 1.57, 1.97, 2.40],
#                  [0.29, 0.55, 0.73, 0.97, 0.98, 1.36, 1.51, 1.71],
#                  [0.11, 0.24, 0.35, 0.49, 0.40, 0.57, 0.59, 0.74]]
#2019           # None, 1,    2,    1&2,  3,    1&3,  2&3,  1&2&3
# scoring_probs = [[0.54, 0.95, 1.17, 1.55, 1.42, 1.79, 2.05, 2.30],
#                  [0.29, 0.56, 0.73, 1.00, 1.00, 1.24, 1.43, 1.64],
#                  [0.11, 0.24, 0.34, 0.46, 0.38, 0.55, 0.61, 0.77]]
#2018           # None, 1,    2,    1&2,  3,    1&3,  2&3,  1&2&3
# scoring_probs = [[0.50, 0.87, 1.14, 1.43, 1.43, 1.79, 1.92, 2.33],
#                  [0.27, 0.53, 0.69, 0.94, 1.00, 1.21, 1.36, 1.48],
#                  [0.10, 0.22, 0.32, 0.45, 0.35, 0.50, 0.58, 0.79]]
#2017           # None, 1,    2,    1&2,  3,    1&3,  2&3,  1&2&3
# scoring_probs = [[0.52, 0.92, 1.17, 1.51, 1.40, 1.83, 2.04, 2.22],
#                  [0.27, 0.53, 0.72, 0.95, 0.98, 1.22, 1.49, 1.63],
#                  [0.11, 0.23, 0.33, 0.45, 0.38, 0.50, 0.58, 0.79]]
#2016           # None, 1,    2,    1&2,  3,    1&3,  2&3,  1&2&3
# scoring_probs = [[0.50, 0.86, 1.13, 1.45, 1.40, 1.72, 1.93, 2.10],
#                  [0.27, 0.52, 0.68, 0.93, 0.98, 1.20, 1.37, 1.54],
#                  [0.11, 0.22, 0.32, 0.42, 0.37, 0.48, 0.55, 0.71]]
#2015           # None, 1,    2,    1&2,  3,    1&3,  2&3,  1&2&3
# scoring_probs = [[0.47, 0.86, 1.11, 1.48, 1.39, 1.71, 2.05, 2.30],
#                  [0.25, 0.50, 0.67, 0.89, 0.97, 1.12, 1.36, 1.59],
#                  [0.10, 0.23, 0.30, 0.43, 0.36, 0.45, 0.56, 0.79]]
#2014           # None, 1,    2,    1&2,  3,    1&3,  2&3,  1&2&3
# scoring_probs = [[0.45, 0.82, 1.07, 1.39, 1.37, 1.78, 1.89, 2.36],
#                  [0.24, 0.48, 0.63, 0.84, 0.94, 1.10, 1.36, 1.51],
#                  [0.09, 0.20, 0.31, 0.40, 0.36, 0.45, 0.51, 0.65]]
#2013           # None, 1,    2,    1&2,  3,    1&3,  2&3,  1&2&3
# scoring_probs = [[0.47, 0.83, 1.11, 1.39, 1.34, 1.76, 1.97, 2.14],
#                  [0.25, 0.51, 0.65, 0.87, 0.94, 1.11, 1.36, 1.54],
#                  [0.10, 0.22, 0.31, 0.40, 0.35, 0.49, 0.55, 0.72]]
# #2012           # None, 1,    2,    1&2,  3,    1&3,  2&3,  1&2&3
# scoring_probs = [[0.50, 0.88, 1.12, 1.47, 1.41, 1.99, 1.99, 2.28],
#                  [0.27, 0.52, 0.69, 0.91, 0.95, 1.39, 1.39, 1.54],
#                  [0.10, 0.23, 0.32, 0.45, 0.35, 0.58, 0.58, 0.78]]
# #2001           # None, 1,    2,    1&2,  3,    1&3,  2&3,  1&2&3
# scoring_probs = [[0.53, 0.92, 1.17, 1.53, 1.51, 1.87, 2.04, 2.43],
#                  [0.29, 0.55, 0.71, 0.91, 0.98, 1.24, 1.46, 1.65],
#                  [0.12, 0.25, 0.35, 0.44, 0.39, 0.52, 0.62, 0.81]]
players = {}
teams_log = {}
scoring_probs = []

# Alrighty! These are gonna need to be park adjusted
# Compute the scoring probabilities for each stadium file. Shouldn't actually be that bad, I guess...
# Still doesn't sound fun though. 

def get_expected_run_value(outs, runners) :
    num_outs = int(outs)
    if num_outs == 3:
        return 0
    if runners[0] == "":
        if runners[1] == "" and runners[2] == "":
            return scoring_probs[num_outs][0]
        elif runners[1] != "" and runners[2] == "":
            return scoring_probs[num_outs][2]
        elif runners[1] == "" and runners[2] != "":
            return scoring_probs[num_outs][4]
        elif runners[1] != "" and runners[2] != "":
            return scoring_probs[num_outs][6]
    elif runners[0] != "":
        if runners[1] == "" and runners[2] == "":
            return scoring_probs[num_outs][1]
        elif runners[1] != "" and runners[2] == "":
            return scoring_probs[num_outs][3]
        elif runners[1] == "" and runners[2] != "":
            return scoring_probs[num_outs][5]
        elif runners[1] != "" and runners[2] != "":
            return scoring_probs[num_outs][7]

def result_expected_run_value(outs, dests):
    num_outs = int(outs)
    runner_dests = [""] * 3
    for i in range(3):
        if 0 < int(dests[i]) < 4:
            runner_dests[int(dests[i]) - 1] = "runner"
    return get_expected_run_value(num_outs, runner_dests)


def rbi_efficiency(event_log):
    for at_bat in event_log:
        parsed_at_bat = at_bat.split(',')
        inning_outs = parsed_at_bat[4]
        batter = parsed_at_bat[10].strip('\"')
        rbi = int(parsed_at_bat[43])
        outs = parsed_at_bat[40]
        runner_dests = parsed_at_bat[58:62]
        end_play_outs = int(inning_outs) + int(outs)
        runners = parsed_at_bat[26:29]
        for i in range(3):
            runners[i] = runners[i].strip('\"')

        if rbi > 0:
            initial_expected_runs = get_expected_run_value(inning_outs, runners)
            result_expected_runs = result_expected_run_value(end_play_outs, runner_dests)
            net_increase = rbi + result_expected_runs - initial_expected_runs 
            if (players.get(batter) == None):
                players.update({batter: [net_increase, rbi]})
            else:
                players.update({batter: [players[batter][0] + net_increase, players[batter][1] + rbi]})
    
# Also add in positive and negative sections on their own - no sense penalizing hitters with crap teams (hi Jose Abreu)

def run_expected_added_team(event_log):
    for at_bat in event_log:
        parsed_at_bat = at_bat.split(',')
        home_team = parsed_at_bat[0][1:4]
        away_team = parsed_at_bat[1]
        batting_team = parsed_at_bat[3]
        inning_outs = parsed_at_bat[4]
        rbi = int(parsed_at_bat[43])
        outs = parsed_at_bat[40]
        runner_dests = parsed_at_bat[58:62]
        end_play_outs = int(inning_outs) + int(outs)
        runners = parsed_at_bat[26:29]
        atbat_end_flag = parsed_at_bat[35].strip('\"')
        team = ""
        if (batting_team == 0):
            team = away_team
        else:
            team = home_team
        for i in range(3):
            runners[i] = runners[i].strip('\"')

        if (atbat_end_flag == "T") :
            initial_expected_runs = get_expected_run_value(inning_outs, runners)
            result_expected_runs = result_expected_run_value(end_play_outs, runner_dests)
            net_change = rbi + result_expected_runs - initial_expected_runs 
            if (net_change >= 0):
                if (teams_log.get(team) == None):
                    teams_log.update({team: [net_change, 0, rbi]})
                else:
                    teams_log.update({team: [teams_log[team][0] + net_change, teams_log[team][1], teams_log[team][2] + rbi]})
            else:
                if (teams_log.get(team) == None):
                    teams_log.update({team: [0, net_change, rbi]})
                else:
                    teams_log.update({team: [teams_log[team][0], teams_log[team][1] + net_change, teams_log[team][2] + rbi]})                
        else: 
            baserunning = parsed_at_bat[66:75]
            initial_expected_runs = get_expected_run_value(inning_outs, runners)
            result_expected_runs = result_expected_run_value(end_play_outs, runner_dests)
            net_change = rbi + result_expected_runs - initial_expected_runs 
            
            for i in range(9):
                baserunning[i] = baserunning[i].strip('\"')
                if (baserunning[i % 3] == "T"):
                    runs_scored = 0
                    if (net_change >= 0):
                        if ((i  % 3) == 2):
                            runs_scored = 1
                        if (teams_log.get(team) == None):
                            teams_log.update({team: [net_change + runs_scored, 0, 0]})
                        else:
                            teams_log.update({team: [teams_log[team][0] + net_change + runs_scored, teams_log[team][1], teams_log[team][2] + 0]})
                    else:
                        if ((i  % 3) == 2):
                            runs_scored = 1
                        if (teams_log.get(team) == None):
                            teams_log.update({team: [0, net_change, 0]})
                        else:
                            teams_log.update({team: [teams_log[team][0] + runs_scored, teams_log[team][1] + net_change, teams_log[team][2] + 0]})
    
                


    return 0    

def run_expected_added(event_log):
    for at_bat in event_log:
        parsed_at_bat = at_bat.split(',')
        inning_outs = parsed_at_bat[4]
        batter = parsed_at_bat[10].strip('\"')
        rbi = int(parsed_at_bat[43])
        outs = parsed_at_bat[40]
        runner_dests = parsed_at_bat[58:62]
        end_play_outs = int(inning_outs) + int(outs)
        runners = parsed_at_bat[26:29]
        atbat_end_flag = parsed_at_bat[35].strip('\"')

        for i in range(3):
            runners[i] = runners[i].strip('\"')

        if (atbat_end_flag == "T") :
            initial_expected_runs = get_expected_run_value(inning_outs, runners)
            result_expected_runs = result_expected_run_value(end_play_outs, runner_dests)
            net_change = rbi + result_expected_runs - initial_expected_runs 
            if (net_change >= 0):
                if (players.get(batter) == None):
                    players.update({batter: [net_change, 0, rbi]})
                else:
                    players.update({batter: [players[batter][0] + net_change, players[batter][1], players[batter][2] + rbi]})
            else:
                if (players.get(batter) == None):
                    players.update({batter: [0, net_change, rbi]})
                else:
                    players.update({batter: [players[batter][0], players[batter][1] + net_change, players[batter][2] + rbi]})                
        else: 
            baserunning = parsed_at_bat[66:75]
            initial_expected_runs = get_expected_run_value(inning_outs, runners)
            result_expected_runs = result_expected_run_value(end_play_outs, runner_dests)
            net_change = rbi + result_expected_runs - initial_expected_runs 
            
            for i in range(9):
                baserunning[i] = baserunning[i].strip('\"')
                if (baserunning[i % 3] == "T"):
                    runs_scored = 0
                    if (net_change >= 0):
                        if ((i  % 3) == 2):
                            runs_scored = 1
                        if (players.get(runners[i % 3]) == None):
                            players.update({runners[i % 3]: [net_change + runs_scored, 0, 0]})
                        else:
                            players.update({runners[i % 3]: [players[runners[i % 3]][0] + net_change + runs_scored, players[runners[i % 3]][1], players[runners[i % 3]][2] + 0]})
                    else:
                        if ((i  % 3) == 2):
                            runs_scored = 1
                        if (players.get(runners[i % 3]) == None):
                            players.update({runners[i % 3]: [0, net_change, 0]})
                        else:
                            players.update({runners[i % 3]: [players[runners[i % 3]][0] + runs_scored, players[runners[i % 3]][1] + net_change, players[runners[i % 3]][2] + 0]})
    
                


    return 0

year = 2012
while year <= 2022:
    players = {}
    teams_log = {}
    scoring_probs = []
    print("Year: " + str(year))
    for team in teams:
        print(team)
        teamFile = open("bfiles/"+str(year)+"eve/"+ str(year) + team + ".BEV", "r")
        games = teamFile.readlines()
        scoring_probs = player_data.scoring_probability_by_stadium(games)
        run_expected_added(games)
        run_expected_added_team(games)
        field_names = ['Player', 'RBIs Added', 'RBIs']

    with open('standardized_teams_'+str(year)+'_rea.csv', 'w') as csv_file: 
        writer = csv.writer(csv_file)
        writer.writerow(["Team", "REA", "RES"])
        for key, value in teams_log.items():
            writer.writerow([key, value[0], value[1]])

    with open('standardized_batters_'+str(year)+'_full_stats.csv', 'w') as csv_file: 
        player_ids = players.keys()
        player_lookup = pybaseball.playerid_reverse_lookup(player_ids, "retro")
        count = 0
        writer = csv.writer(csv_file)
        writer.writerow(["Batter", "REA", "RES", "PA", "OPS", "OBP", "SLG", "AVG", "RBI", "HR"])
        for key, value in players.items():
            standard_data = player_data.load_player(key, year)
            writer.writerow([key, value[0], value[1], standard_data.get("plateappearances"), standard_data.get("ops"), standard_data.get("obp"), standard_data.get("slg"), standard_data.get("avg"), standard_data.get("rbi"), standard_data.get("homeruns")])
    
    year += 1
# teamFile = open("bfiles/2022eve/2022COL.BEV", "r")
# games = teamFile.readlines()
# er = player_data.scoring_probability_by_stadium(games)
# print(er)
import csv
import pybaseball
import player_data

teams = ["ANA", "ARI", "ATL", "BAL", "BOS", "CHA", "CHN", "CIN", "CLE", "COL", "DET", "HOU", "KCA", "LAN", "MIA", "MIL", "MIN", "NYA", "NYN", "OAK", "PHI", "PIT", "SDN", "SEA", "SFN", "SLN", "TBA", "TEX", "TOR", "WAS"]

players = {}
teams_log = {}
scoring_probs = [] 

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
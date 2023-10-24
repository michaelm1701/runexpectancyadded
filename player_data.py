import mlbstatsapi
import pybaseball
import requests

from bs4 import BeautifulSoup

player_stats = {}

def load_player(retro_id, year):
    player_lookup = pybaseball.playerid_reverse_lookup([retro_id], "retro")
    mlbam_key = player_lookup['key_mlbam']
    mlb = mlbstatsapi.Mlb()
    stats = ['season', 'career']
    groups = ['hitting', 'pitching']
    params = {'season': year}
    stat_dict = mlb.get_player_stats(mlbam_key[0], stats=stats, groups=groups, **params)
    season_hitting_stat = stat_dict['hitting']['season']
    for k, v in season_hitting_stat.splits[0].stat.__dict__.items():
        player_stats.update({k:v})
    
    return player_stats



def get_outcome_index(runners):
    if runners[0] == "":
        if runners[1] == "" and runners[2] == "":
            return 0
        elif runners[1] != "" and runners[2] == "":
            return 2
        elif runners[1] == "" and runners[2] != "":
            return 4
        elif runners[1] != "" and runners[2] != "":
            return 6
    elif runners[0] != "":
        if runners[1] == "" and runners[2] == "":
            return 1
        elif runners[1] != "" and runners[2] == "":
            return 3
        elif runners[1] == "" and runners[2] != "":
            return 5
        elif runners[1] != "" and runners[2] != "":
            return 7

def runs_scored_on_play(runners) : 
    runs = 0
    for i in range(4):
        if (int(runners[i]) > 3):
            runs += 1
    return runs

def scoring_probability_by_stadium(event_log):
                # None, 1,    2,    1&2,  3,    1&3,  2&3,  1&2&3
    runs_scored = [[0, 0, 0, 0, 0, 0, 0, 0,],
                   [0, 0, 0, 0, 0, 0, 0, 0,],
                   [0, 0, 0, 0, 0, 0, 0, 0,]]
    occurences = [[0, 0, 0, 0, 0, 0, 0, 0,],
                  [0, 0, 0, 0, 0, 0, 0, 0,],
                  [0, 0, 0, 0, 0, 0, 0, 0,]]
    totalpa = len(event_log)
    num_pa = 0
    inning_at_bat = 0
    while num_pa < totalpa:
        inning_end_flag = 0
        parsed_at_bat = event_log[num_pa].split(',')
        outs = int(parsed_at_bat[4])
        runners = parsed_at_bat[26:29]
        for i in range(3):
            runners[i] = runners[i].strip('\"')
        outcome_index = get_outcome_index(runners)
        occurences[outs][outcome_index] += 1
        game_end_1 = parsed_at_bat[79]
        while (inning_end_flag == 0):
            ab = event_log[num_pa + inning_at_bat].split(',')
            runner_dests = ab[58:62]
            runs = runs_scored_on_play(runner_dests)
            outs_1 = int(ab[4])
            runs_scored[outs][outcome_index] += runs
            outs_recorded = int(ab[40])
            game_end_1 = ab[79]
            inning_at_bat += 1
            if (outs_1 + outs_recorded >= 3 or game_end_1.strip('\"') == "T"):
                inning_at_bat = 0
                num_pa += 1
                inning_end_flag = 1
                
        
    expected_runs = [[0, 0, 0, 0, 0, 0, 0, 0,],
                   [0, 0, 0, 0, 0, 0, 0, 0,],
                   [0, 0, 0, 0, 0, 0, 0, 0,]]
    for i in range(0, 3):
        for j in range(0, 8):
            if (occurences[i][j] == 0) :
                expected_runs[i][j] = 0
            else:
                expected_runs[i][j] = (runs_scored[i][j] * 1.0) / occurences[i][j]

    return expected_runs

    # Go from at bat to end of inning
    # Tally every run that was scored after that situation occured
    # Will need to acccount for identical outcomes
    # Reset if next at bat is leadoff batter, or if game ends
    # 24 possible base/out situations
    # Have dictionary or array for each inning


    return 0



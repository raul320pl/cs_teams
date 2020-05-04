# Counter Strike team selector by raul302pl.
#
# Enjoy for free!

import itertools
import json

class Player:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills

    def rank(self):
        return sum(self.skills)
    
    def __str__(self):
        return "{0} [{1:03.2f}]".format(self.name, self.rank())
    
    def __hash__(self):
        return hash(self.name)
 

class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players

    def rank(self):
        return sum(x.rank() for x in self.players)

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return "Team {0} {1: 03.2f} {2}".format(self.name, self.rank(), ", ".join([str(x) for x in self.players]))


def prepare_teams(players):    
    for n, team in enumerate(itertools.combinations(players,len(players)//2)):            
        ct_team = Team("CT{:0>2d}".format(n), team)
        tt_team = Team("TT{:0>2d}".format(n), tuple(players - set(team)))
        team_set = [ct_team, tt_team, ct_team.rank() - tt_team.rank()]
        yield team_set


def read_data(filename):
    print("Reading input data from {}...\n".format(filename))
    try:
        with open(filename) as json_file:
            data = json.load(json_file)
            # read config section (weights and others..
            config = {}
            for field, val in  data['config'].items():
                config[field]=val            
            # read players
            players = set()
            for player in data['players']: 
                skill_array = [] 
                for skill, value in player['skills'].items():
                    if skill in config:
                        skill_array.append(float(value)*float(config[skill]))                        
                    else:
                        skill_array.append(float(value))                                         
                players.add(Player(player['name'],skill_array))
            #list players                
        return (prepare_teams(players),config, players)
    except Exception as e:
        print("Reading error!")
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)
        return ([],[],[])

if __name__ == "__main__":
    teams, config, players = read_data("data.json")
    if players:
        print("Players:")
        for p in players:
            print(" - {}".format(p))
    print()
    if teams:
        teams = list(teams)
        # sort by team diff
        teams.sort(key=lambda x: abs(x[-1]))
        # set print treshold
        if "show_teams" in config:
            teams = teams[:int(config["show_teams" ])]
        for i, team in enumerate(teams):            
            print("Selection {0} - diff {1: 03.3f}".format(i+1,team[-1]))
            print(" - {0}".format(team[0]))
            print(" - {0}".format(team[1]))
            print("")
            
    input("press enter to exit ... ")   

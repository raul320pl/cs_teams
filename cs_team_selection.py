# Counter Strike team selector by raul302pl.
#
# Enjoy for free!

import itertools
 
class Player:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills

    def rank(self):
        return sum(self.skills)
    
    def __lt__(self, other):
        return self.rank() < other.rank()

    def __eq__(self, other):
        return self.rank() == other.rank()  and self.name == other.name
    
    def __ne__(self, other):
        return self.rank() != other.rank() or self.name != other.name

    def __gt__(self, other):
        return self.rank() > other.rank()

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
    
    def __lt__(self, other):
        return self.rank() < other.rank()

    def __le__(self, other):
        return self.rank() <= other.rank()

    def __eq__(self, other):
        return self.rank() == other.rank()
    
    def __ne__(self, other):
        return self.rank() != other.rank()

    def __gt__(self, other):
        return self.rank() > other.rank()

    def __ge__(self, other):
        return self.rank() >= other.rank()

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return "Team {0} {1: 03.2f} {2}".format(self.name, self.rank(), ", ".join([str(x) for x in self.players]))


def prepare_teams(players):
    for n, team in enumerate(itertools.combinations(players,len(players)//2)):
        rest_of_players =  tuple(players - set(team))
        ct_team = Team("CT{:0>2d}".format(n), team)
        tt_team = Team("TT{:0>2d}".format(n), rest_of_players )
        team_set = [ct_team, tt_team, ct_team.rank() - tt_team.rank(),ct_team.rank(),tt_team.rank()] 
        yield team_set


def skills(comm=1, precision=1, tactics=1, relyability=1, reflex=1, team_play=1):
    return [
            comm * 0.5,
            precision *0.9,
            tactics * 0.6,            
            relyability * 1.0,
            reflex * 0.8,
            team_play * 1.0
            ]


players = {Player("~YEGO",     skills(comm=10,precision=10,tactics=10,relyability=10,reflex=10,team_play=10)),
            Player("Himmlerek",skills(comm=7, precision=8, tactics=8, relyability=8, reflex=10,team_play=10)),            
            Player("Adam",     skills(comm=5, precision=7, tactics=6, relyability=8, reflex=8 ,team_play=10)),
            Player("DaneQ",    skills(comm=5, precision=7, tactics=6, relyability=8, reflex=8 ,team_play=1)),
            Player("Kris",     skills(comm=5, precision=7, tactics=6, relyability=8, reflex=8 ,team_play=1)),
            Player("Powolniak",skills(comm=4, precision=5, tactics=6, relyability=8, reflex=8 ,team_play=1)),
            Player("Kuba",     skills(comm=5, precision=5, tactics=6, relyability=8, reflex=8 ,team_play=1)),
            Player("Infinity", skills(comm=3, precision=7, tactics=8, relyability=8, reflex=8 ,team_play=1)),
            Player("Szewa",    skills(comm=1, precision=5, tactics=6, relyability=8, reflex=1 ,team_play=1)),
            Player("Perun",    skills(comm=2, precision=5, tactics=8, relyability=8, reflex=1 ,team_play=1)),
            Player("Bert",     skills(comm=3, precision=7, tactics=6, relyability=8, reflex=1 ,team_play=1)),
           }

#display teams
teams_sets = list(prepare_teams(players))
teams_sets.sort(key=lambda x: abs(x[-3]))
MAX_DIFF = 2.0
skipped = 0
print("Prepared {} team combinations (show diff < {})".format(len(teams_sets),MAX_DIFF))
for i,ts in enumerate(teams_sets):        
    if abs(ts[-3]) < MAX_DIFF:
        print("Selection {0} - diff {1: 03.3f}".format(i+1,ts[-3]))
        print(" - {0}".format(ts[0]))
        print(" - {0}".format(ts[1]))
        print("")
    else:
        skipped += 1
if skipped == len(teams_sets):
    print("Team differences to high")
elif skipped>0:
    print("Skipped {} team combinations.".format(skipped))
    
              
              
              

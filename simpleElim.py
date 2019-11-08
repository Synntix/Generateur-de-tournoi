import random
from copy import deepcopy

def getMatchlistSimpleElim(players):
    initalPlayers=deepcopy(players)
    Matchlist = []
    tempMatch = []
    while len(initalPlayers) != 0:
         j1 = random.randint(0, len(initalPlayers)-1)
         tempMatch.append(initalPlayers[j1])
         initalPlayers.remove(initalPlayers[j1])

         j2 = random.randint(0, len(initalPlayers)-1)
         tempMatch.append(initalPlayers[j2])
         initalPlayers.remove(initalPlayers[j2])
         Matchlist.append(tempMatch)
         tempMatch = []

         if len(initalPlayers) == 1:
             tempMatch.append(initalPlayers[0])

             j2 = random.randint(0, len(players)-1)
             while players[j2] == initalPlayers[0]:
                 j2 = random.randint(0, len(players)-1)
             initalPlayers.remove(initalPlayers[0])
             tempMatch.append(players[j2])
             Matchlist.append(tempMatch)
             tempMatch = []
    return Matchlist


print(getMatchlistSimpleElim(["Paul","Pierre","Jaques","Bite","Pouasson","Julien","Alexandre","Alice"]))

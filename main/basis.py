# -*- coding: utf-8 -*-
from models import Tour
def toss_tour1(players):
    i=0
    last=len(players)/2
    res=[]
    tour_num=1
    while i<last:
        tour=Tour(tour=tour_num,player1=players[i],player2=players[last+i])
        tour.save()
        res.append(tour)
        i+=1
    l=len(players)
    if l%2:
        tour=Tour(tour=tour_num,player1=players[l-1],points=1)
        tour.save()
        res.append(tour)
    return res

def toss_next(pair_list,tour_num):
    #making 3 list (0,0.5,1)
    res={'winners':[],'drawers':[],'losers':[]}
    for item in pair_list:
        if item.points==1:
            res['winners'].append(item.player1)

            # not null
            if item.player2:
                res['losers'].append(item.player2)
        elif item.points==0.5:
            res['drawers'].append(item.player1)
            res['drawers'].append(item.player2)
        else:
            res['losers'].append(item.player1)
            res['winners'].append(item.player2)

    #send extra user to the end of list
    if (len(res['winners'])%2):
        res['drawers'].insert(0,res['winners'][-1])
        res['winners']=res['winners'][0:-1]
    if (len(res['drawers'])%2):
        res['losers'].insert(0,res['drawers'][-1])
        res['drawers']=res['drawers'][0:-1]

    #toss
    def _tour(players):
        i=0
        last=len(players)/2
        res=[]
        while i<last:
            tour=Tour(tour=tour_num,player1=players[i],player2=players[last+i])
            tour.save()
            res.append(tour)
            i+=1
        l=len(players)
        if l%2:
            tour=Tour(tour=tour_num,player1=players[l-1],points=1)
            tour.save()
            res.append(tour)
        return res

    toss=_tour(res['winners'])+_tour(res['drawers'])+_tour(res['losers'])
    return toss

#================================================
def _get_probability_ex(member):
        #expectations from player A for tournament

        def e_a(a,b):
            #expected raiting A

            return 1/(1+10**(float(b-a)/400))


        #TODO: optimize that
        pe=0
        name=member.name
        elo=member.elo
        tours=Tour.objects.all()
        for item in tours:

            #find competitor
            if name in item.player1.name:
                # get "p"

                #if "empty" player
                if item.player2:
                    elo2=item.player2.elo
                else:
                    elo2=elo

                p=e_a(elo,elo2)
                pe+=p

            elif item.player2 and name in item.player2.name:

                elo2=item.player1.elo
                p=e_a(elo,elo2)
                pe+=p
        return pe

def _get_points(member):
    #all points

    points=0
    tours=Tour.objects.all()
    name=member.name
    for item in tours:
        if name in item.player1.name:
            points+=item.points

        elif item.player2 and name in item.player2.name and item.points==0.5:
            points+=item.points

    return points

def get_elo_new(member):
        from chess.settings import CHESS_K

        pe=_get_probability_ex(member)
        points=_get_points(member)
        elo=member.elo
        k=CHESS_K # default coefficient
        result=elo+k*(points-pe)
        return int(result)
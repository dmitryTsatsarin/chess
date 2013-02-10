# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required

__author__ = 'dmitry'
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from models import Member, Tournament, Tour
from forms import MemberForm
from django.contrib import messages
import basis

def home(request):

    return render_to_response('main.html',
        {},
        context_instance=RequestContext(request))

@login_required
def add_member(request):
    memberForm=None
    tournament_start=False

    try:
        tournament_start=Tournament.objects.get(pk=1).start
    except Tournament.DoesNotExist:
        tournament_start=False
    if (tournament_start):
        messages.error(request,'Error! Tournament is started already')
    else:
        if request.POST:
            memberForm=MemberForm(request.POST)
            if memberForm.is_valid():
                memberForm.save()
                messages.success(request,'Information is added')
                memberForm=MemberForm()
            else:
                messages.error(request,'Error in fields')
        else:
            memberForm=MemberForm()





    return render_to_response('member_add.html',
        {'memberForm':memberForm},
        context_instance=RequestContext(request))

def show_list_members(request):

    members=Member.objects.order_by('name')
    return render_to_response('members_list.html',
        {'members':members},
        context_instance=RequestContext(request))


@login_required
def tournament_start(request):
    import math

    members_count=Member.objects.all().count()

    #count=log2 N + log2 K, to find out who is winner log2 K=1
    if members_count>=2:
        tour_count=int(round(math.log(members_count,2))+1)

        try:
            tournament=Tournament.objects.get(pk=1)
            if not tournament.start:
                tournament.start=True
                tournament.tour_closed=0
                tournament.tour_last=tour_count
                tournament.save()
        except Tournament.DoesNotExist:
            Tournament.objects.create(start=True, tour_closed=0,tour_last=tour_count)
        messages.success(request,'Tournament is started')

    else:
        messages.error(request,'Must be 2 members at least')

    return render_to_response('tournament.html',
        {},
        context_instance=RequestContext(request))

@login_required
def tournament_judge(request):
    template_file='tournament_judge.html'
    tournament,_=Tournament.objects.get_or_create(pk=1)
    tour_num=_check_tour()

    tour=None
    form_show_flag=True
    start_flag=False

    if (tournament.start):
        if request.POST:
            points_dirty=[]
            tour_num=int(request.POST.get('tour_num',0))
            import re
            p=re.compile(r'points_(\d+)')
            for key in request.POST.keys():
                m=p.match(key)
                if m:
                    points_dirty.append({'id':m.group(1),'points':float(request.POST[key])})
            # validate
            validate=True
            for item in points_dirty:
                if item['points'] not in  [0,0.5,1]:
                    messages.error(request,'Uncorrected points. "0", "0.5", "1" are available"')
                    validate=False
            if validate:
                for item in points_dirty:
                    tour_item=Tour.objects.get(pk=item['id'])
                    tour_item.points=item['points']
                    tour_item.save()
                messages.success(request,'Success! Data saved')
                form_show_flag=False

                # go to next tour
                tournament.tour_closed=tour_num
                tournament.save()

            else:
                tour=Tour.objects.filter(tour=tour_num)


            #
        else:
            if tour_num<=tournament.tour_last:
                pairs=Tour.objects.filter(tour=tour_num)
                if not pairs.exists():
                    if tour_num==1:
                        members=Member.objects.all()
                        tour=basis.toss_tour1(members)
                    else:
                        pairs_old=Tour.objects.filter(tour=tour_num-1)
                        tour=basis.toss_next(pairs_old,tour_num)
                else:
                    tour=pairs
            else:
                template_file='tournament_finished.html'
                tournament.start=False
                tournament.save()
                messages.info(request, 'Tournament is finished')


    else:
        template_file='tournament_judge.html'
        messages.error(request,'Error! Tournament is not started')
        form_show_flag=False
        start_flag=True

    return render_to_response(template_file,
        {'tour':tour, 'tour_num':tour_num,'form_show_flag':form_show_flag,'start_flag':start_flag},
        context_instance=RequestContext(request))

def _check_tour():
    tour_closed=Tournament.objects.get(pk=1).tour_closed
    tour_num=tour_closed if tour_closed else 0

    tour_num+=1
    return tour_num

def _set_new_elo_rating(members):
    res=[]
    for member in members:
        elo=basis.get_elo_new(member)
        member.elo_new=elo
        member.save()

def tournament_results(request):

    # members
    members=Member.objects.order_by('name')

    #tours
    tournament,_=Tournament.objects.get_or_create(pk=1)
    tour_num=tournament.tour_closed if tournament.tour_closed else 0
    tours=Tour.objects.filter(tour__in=xrange(1,tour_num+1))

    #new ELO rating
    elo_new_flag=False
    if tournament.tour_closed and tournament.tour_closed==tournament.tour_last:
        if Member.objects.filter(elo_new__isnull=True).exists():
            _set_new_elo_rating(members)
        elo_new_flag=True

    return render_to_response('tournament_results.html',
        {'members':members,'tours':tours,'elo_new_flag':elo_new_flag},
        context_instance=RequestContext(request))


@login_required
def tournament_zeroing(request):

    members=Member.objects.all()
    for member in members:
        member.elo_new=None
        member.save()

    tournament=Tournament.objects.get(pk=1)
    tournament.start=False
    tournament.tour_closed=None
    tournament.tour_last=None
    tournament.save()

    Tour.objects.all().delete()
    messages.success(request,'Tournament is deleted')

    return render_to_response('tournament.html',
        {},
        context_instance=RequestContext(request))

import feedparser

from datetime import datetime
import time

from bugzilla.agents import BMOAgent
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import simplejson

from .models import Bug, BuildStatus

milestones = [
'2013-01-03',
'2013-01-10',
'2013-01-17',
'2013-01-24',
'2013-01-31',
'2013-02-07',
'2013-02-14',
'2013-02-28',
'2013-03-14',
'2013-03-21',
'2013-03-28',
'2013-04-04',
'2013-04-11',
'2013-04-18',
'2013-04-25',
'2013-05-02',
'2013-05-09',
'2013-05-16',
'2013-05-23',
'2013-05-30',
'2013-06-06',
'2013-06-13',
'2013-06-20',
'2013-06-27',
'2013-07-04',
'2013-07-11',
'2013-07-18',
'2013-08-01',
'2013-08-06',
]

def update_ci_numbers():
    source = "https://ci.mozilla.org/job/marketplace/rssAll"

    feed = feedparser.parse(source)

    for i in feed['entries']:

        x = BuildStatus()
        x.project = "marketplace"
        x.published = time.strftime('%Y-%m-%d %H:%M:%S', i['published_parsed'])
        x.status = "yes"
        x.save()


    if feed['status'] not in [200] or feed['bozo'] == 1:
        print "Got an error: %s" % feed['status']
        raise



def get_bug_counts_from_bugzilla():

    bmo = BMOAgent()

    for milestone in milestones:
        options = {
            'target_milestone': milestone,
            'product':          'Marketplace',
            'resolution':       'FIXED',
            'include_fields':   'id,assigned_to,whiteboard',
        }

        buglist = bmo.get_bug_list(options)

        print "Found %s bugs in %s" % (len(buglist), milestone)

        for bug in buglist:
            x = Bug()
            x.id = bug.id
            x.assignee = bug.assigned_to
            x.status = "RESOLVED"
            x.milestone = milestone
            x.whiteboard = bug.whiteboard
            x.save()

    return []

def json_bugs(request):

    # Needs to be defined for d3
    people = {
        'ashort',
        'charmston',
        'cvan',
        'dspasovski',
        #'kumar.mcmillan',
        'mattbasta',
        'mpillard',
        'ngoke',
        'robhudon.mozbugs'
        #'scolville',
    }
    x = {}

    for bug in Bug.objects.filter(milestone__gte=datetime(2013, 05, 01)):
        date = bug.milestone.strftime('%Y-%m-%d')

        if date not in x:
            x[date] = {}
            #x[date]["other"] = 0
            for i in people:
                x[date][i] = 0

        if bug.assignee in people:
            x[date][bug.assignee] += 1
        else:
            pass
            #x[date]["other"] += 1

    data = []
    for date in x:
        for assignee in x[date]:
            data.append({'date': date, 'key': assignee, 'value': x[date][assignee]})

    data.sort()
    y = simplejson.dumps(data)
    return HttpResponse(y, mimetype='application/json')


def home(request):
    """Engineering home."""
    data = {
        'milestones': milestones
    }
    return render(request, 'engineering/home.html', data)


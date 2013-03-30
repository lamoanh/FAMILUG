#!/usr/bin/env python
#-*-encoding: utf-8 -*-

from datetime import date as dtdate
from datetime import timedelta
import urllib
from xml.dom import minidom

from pprint import pprint

# find this token in git.vccloud.vn, "News Feed" item below right column
GIT_TOKEN = 'c9sArqzmoVMqgy7BUjyh'

GIT_URL = "http://git.vccloud.vn/dashboard.atom?private_token="+GIT_TOKEN

""" A simple script auto generate data for 
    reporting weekly at BBTeam - VCCloud"""

# TODO: get data from git and wiki, teamspace
# put them all in template then send

def get_week_boundary(day_in_week=dtdate.today()):
    """ Return a tuple contains Monday and Saturday day of a week """
    dow = day_in_week.weekday()

    mon_of_week = day_in_week - timedelta(dow)
    sat_of_week = mon_of_week + timedelta(5)
    date_format = "%Y/%m/%d"

    return (mon_of_week.strftime(date_format), 
            sat_of_week.strftime(date_format))

def send_request(url):
    return urllib.urlopen(url) 

# get data (branch name + commit-content, commit-time) from git
# lists or json ???
# structure:
# [
#     [
#         'branch name 1', 
#         'updated time 1', 
#         [
#             ['commit content 1','commit time 1'],
#             ['commit content 2','commit time 2'],
#             ['commit content n','commit time n'],
#         ]
#     ],
#     [
#         'branch name n', 
#         'updated time n', 
#         [
#             ['commit content 1','commit time 1'],
#             ['commit content 2','commit time 2'],
#             ['commit content n','commit time n'],
#         ]
#     ]
# ]

def get_from_git():
    url = GIT_URL
    res = send_request(url)
    """ parse XML:
    <entry>
        <id>tag:git.vccloud.vn,2013-03-29:878</id>
        <link href="http://git.vccloud.vn/lamdt/vpn/commit/edf2b1ce83f2fa8fdddd5019af958d59870946f9"/>
        <title>LamDT pushed to branch master at vpn</title>
        <updated>2013-03-29T04:30:49Z</updated>
        <media:thumbnail width="40" height="40" url="http://www.gravatar.com/avatar/202e3cd5282ce662ab7dbac73029e545?s=40&amp;d=mm"/>
        <author>
            <name>LamDT</name>
            <email>lamdt@vccloud.vn</email>
        </author>
        <summary type="xhtml">
            <div xmlns='http://www.w3.org/1999/xhtml'>
                <p>
                    <strong>at VCC</strong>
                    <a href="/lamdt/vpn/commit/edf2b1ce83f2fa8fdddd5019af958d59870946f9">(#edf2b1ce83f)</a>
                    <i>at 2013-03-29 11:30:48</i>
                </p>
                <blockquote><p>button fix for chrome</p></blockquote>
            </div>
        </summary>
    </entry>
    """
    result = []
    dom = minidom.parse(res)
    item_list = dom.getElementsByTagName('entry')
    
    for node in item_list:
        entry = []
        # get title
        title = node.getElementsByTagName('title')
        entry.append(title[0].firstChild.nodeValue)

        # # get update
        update = node.getElementsByTagName('updated')
        entry.append(update[0].firstChild.nodeValue)

        # get commits
        entry_commits = []
        commits = node.getElementsByTagName('div')

        for commit in commits:
            entry_commit_one = []

            # get commit time
            for commit_time in commit.getElementsByTagName('i'):
                # print commit_time.firstChild.nodeValue
                entry_commit_one.append(commit_time.firstChild.nodeValue)

            # get commit content
            for commit_content in commit.getElementsByTagName('p'):
                # print commit_content.firstChild.nodeValue
                entry_commit_one.append(commit_content.firstChild.nodeValue)

            entry_commits.append(entry_commit_one)

        entry.append(entry_commits)
        
        # result concatenation
        result.append(entry)

    pprint (result)


def get_subject(wbdr=get_week_boundary()):
    # print get_from_git('c9sArqzmoVMqgy7BUjyh')
    # return "Báo cáo tuần (%s -> %s)" % wbdr
    return get_from_git()


if __name__ == "__main__":
    get_subject()
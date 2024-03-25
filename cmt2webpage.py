

#---
#layout: default
#title: AI for Earth Sciences
#description: org
#---
#
### Sensors and Sampling Schedule
#
#| Start | End | Type | Speaker | Title and Info |
#| ---- | ---- | --------- | ------------- | ----------------- |
#| 6:55 | 6:58 | Intro | Johanna Hansen | Session Overview and Introduction |
#| 6:58 | 7:22 | Keynote | [Yogesh Girdhar](http://warp.whoi.edu/) | [Curious Robots for Scientific Sampling](#yogesh-girdhar) |

import pandas as pd
import numpy as np
from glob import glob
import os
from collections import OrderedDict
import pytz
from datetime import datetime
#from icalendar import vDatetime, Calendar, Event
import shutil
from IPython import embed
p = pd.read_csv("AI4Earth_Papers_all.csv") # export from google doc which was from cmt
a = pd.read_csv("abstracts.csv")
abstracts = a[['Paper ID', 'Abstract', 'Paper Title']]
# some rows are nan because they are breaks bt sessions
isna = [pd.notna(x) for x in p['Authors']]
papers = p[isna]
# we only want to work with accepts
papers = papers[papers['Accept/Reject'] != 'reject']
# fix author names
# collect abstracts
papers.loc[papers['Primary Subject Area'] == 'Sensors & Sampling', 'Primary Subject Area'] = 'Sensors'
# dont merge since some dont have abstracts
#papers = pd.merge(papers, abstracts, on='Paper ID')
sessions = ['Welcome',
           'Sensors', 
            'Ecology', 
            'Water', 
            'Keynote', 
            'Atmosphere', 
            'Theory',
            'People-Earth',
            'Solid-Earth', 
            'Datasets', 
            'Closing']

# make normal dict of tuples for human name, start, end times
# ((start end times of session), (start end times of discussion))
session_times = {
        'Welcome':      ('Opening Remarks',       ('06:45', '06:55'),     ()),
        'Sensors':      ('Sensors & Sampling',    ('06:55', '08:55'),     ('08:20', '08:55')),
        'Ecology':      ('Ecology',               ('08:55', '10:55'),     ('10:30', '10:55')),
        'Water':        ('Water',                 ('10:55', '12:45'),     ('12:20', '12:45')),
        'Keynote':      ('Keynote: Milind Tambe', ('12:45','13:25'),      ('13:15', '13:25')),
        'Atmosphere':   ('Atmosphere',             ('13:25','15:25'),     ('14:55', '15:25')),
        'Theory':       ('Theory',                 ('15:25','17:20'),     ('17:00', '17:20')),
        'People-Earth': ('People-Earth',           ('17:20','18:00'),     ('15:25', '18:00')),
        'Solid-Earth':  ('Solid-Earth',            ('18:00','19:00'),     ('16:45','19:00')),
        'Datasets':     ('Benchmark Datasets',     ('19:00','20:55'),     ('20:30', '20:55')),
        'Closing':      ('Closing Remarks',        ('20:55','21:00'),     ()),
        } 


session_panelists = {'People-Earth':[
                  '<a href="https://teamcore.seas.harvard.edu/people/milind-tambe">Milind Tambe (Harvard, Google)', 
                  '<a href="http://kammen.berkeley.edu/">Dan Kammen (Berkeley)', 
                  '<a href="https://deleolab.stanford.edu/people">Giulio De Leo (Stanford)'],
                  'Sensors': ['<a href="https://www.cim.mcgill.ca/~mrl/"> Greg Dudek (McGill, SamsungAI)']}
top = """
# Overview Schedule 
## All times are in PST (Vancouver time)
| Start | End | Session | Session Chair | Keynotes / Panelists  |   
| ---- | ---- | --------- | ------------------- |  --------------------------- | 
| 06:45 | 06:55 | [Welcome](#welcome)  | S. Karthik Mukkavilli | --- |  
| [06:55](https://calendar.google.com/event?action=TEMPLATE&tmeid=MzBncW5hZGphamNhcTM0NWlrOXJwZWRpYzYgYWk0ZWFydGhzY2llbmNlQG0&tmsrc=ai4earthscience%40gmail.com) | 08:55 | [Sensors and Sampling](#sensors) | Johanna Hansen | Yogesh Girdhar, Hannah Kerner, Renaud Detry, & Greg Dudek |    
| [08:55](https://calendar.google.com/event?action=TEMPLATE&tmeid=MGx1ajVkdDBidGt0aThmZ2NvZ291dWczcWMgYWk0ZWFydGhzY2llbmNlQG0&tmsrc=ai4earthscience%40gmail.com) | 10:55 | [Ecology](#ecology) | Natasha Dudek |  Dan Morris & Giulio De Leo |   
| [10:55](https://calendar.google.com/event?action=TEMPLATE&tmeid=MXRnczQzNjQ2NmJpN2ZwbWI0cmJvOWd0b2MgYWk0ZWFydGhzY2llbmNlQG0&tmsrc=ai4earthscience%40gmail.com) | 12:45 | [Water](#water) | S. Karthik Mukkavilli | Pierre Gentine  |   
| [12:45](https://calendar.google.com/event?action=TEMPLATE&tmeid=MGQwc2ViYWF2NmR1am40bnZsdWNvajl0a2kgYWk0ZWFydGhzY2llbmNlQG0&tmsrc=ai4earthscience%40gmail.com) | 13:25 | [Keynote: Milind Tambe](#keynote)  | S. Karthik Mukkavilli | Milind Tambe |  
| [13:25](https://calendar.google.com/event?action=TEMPLATE&tmeid=NDMyOHRtMmtrazlrM3V1ZmlxODV1N3JpajggYWk0ZWFydGhzY2llbmNlQG0&tmsrc=ai4earthscience%40gmail.com) | 15:25 | [Atmosphere](#atmosphere)  | Tom Beucler | Michael Pritchard & Elizabeth Barnes |  
| [15:25](https://calendar.google.com/event?action=TEMPLATE&tmeid=NGx1ZTNwanZuc3RnOTltYnNwZmV0bm51aWEgYWk0ZWFydGhzY2llbmNlQG0&tmsrc=ai4earthscience%40gmail.com) | 17:20 | [ML Theory](#theory) | Karthik Kashinath | Stephan Mandt & Rose Yu |  
| [17:20](https://calendar.google.com/event?action=TEMPLATE&tmeid=MDZhdDFtNmRwamd2NnRpdmJiaGZlbnFjZTEgYWk0ZWFydGhzY2llbmNlQG0&tmsrc=ai4earthscience%40gmail.com) | 18:00 | [People-Earth](#people-earth)          | Mayur Mudigonda | Dan Kammen, Milind Tambe, & Giulio De Leo  |  
| [18:00](https://calendar.google.com/event?action=TEMPLATE&tmeid=NWo0NGNibDY5a3A2dWdiZ2kwcDZ2cWUwb2QgYWk0ZWFydGhzY2llbmNlQG0&tmsrc=ai4earthscience%40gmail.com) | 19:00 | [Solid-Earth](#solid-earth)            | Kelly Kochanski | --- |   
| [19:00](https://calendar.google.com/event?action=TEMPLATE&tmeid=MmlkYWM2Ym4wb284cWtyN3NnaDdlMzk0OWogYWk0ZWFydGhzY2llbmNlQG0&tmsrc=ai4earthscience%40gmail.com) | 20:55 | [Datasets](#datasets)            | Karthik Kashinath | Stephan Rasp |  
| 20:55 | 21:00 | [Closing Remarks](#closing)                  | Organizers  | -- |   

## [Join our slack for live Q&A](https://join.slack.com/t/ai4earth/shared_invite/zt-jkg0i982-VYRAd0HbjCG_6970Hcqfwg)  
## Live stream on [neurips.cc](https://neurips.cc/virtual/2020/protected/workshop_16105.html)
---
"""

zoom = 'https://us02web.zoom.us/j/84740675136?pwd=MGNlSll3T1Z2Q2svTjhTTWoyRTY4QT09'

table = """
<html>
<p style="display:inline";>
<table>
  <colgroup>
  <col span="1" style="width: 1%;">
  <col span="1" style="width: 2%;">
  <col span="1" style="width: 8%;">
  <col span="1" style="width: 20%;">
  <col span="1" style="width: 15%;">
  </colgroup>
  <tr>
    <th>#</th>
    <th>Start Time</th>
    <th>Video</th>
    <th>Title</th>
    <th>Author(s)</th>
    <th>Details</th>
  </tr>
"""

abs_ids = list(abstracts['Paper ID'].astype(np.int))
default_details = {'Introduction':'Short introduction to the session', 
        'Discussion':'Post your questions to slack to hear from our authors in live Q&A.', 
                   'Welcome':'Welcome', 
                   'Closing':'Closing & Thanks', 
                   }

long_length = int(len(default_details['Discussion']))
# paper have the ID\CameraReady in beginning of name
cam_readys = glob('papers/*CameraReady*.pdf')
fo = open('schedule.md', 'w') 
fo.write(top)
tz = pytz.timezone('US/PAcific')
sitename = 'https://ai4earthscience.github.io/neurips-2020-workshop/'
for xx, session in enumerate(sessions):
    #fo = open('sessions/{}.html'.format(session.lower()), 'w') 
    session_name = session.title()
    fo.write("\n\n---".format(session_name))
    fo.write("\n\n## {}  \n\n\n  ".format(session_name))
    fo.write(table)
    session_talks = papers.loc[papers['Primary Subject Area'] == session]
    order = sorted(list(session_talks['Order'].to_numpy().astype(np.int)))
    panelists = []
    if session in session_panelists.keys():
        panelists.extend(session_panelists[session])
    for ind in order:
        talk = session_talks.loc[session_talks['Order'] == ind]
        paper_id = talk['Paper ID'].to_numpy()[0]
        talk_type = talk['Type'].to_numpy()[0].title()
        talk_time = talk['Time'].to_numpy()[0]
        if talk_time == 'On-demand':
            talk_time = '---'
        longform = "" 
        longline = ""
        title = talk['Paper Title'].to_numpy()[0]#.title() # title resulted in 'S  in "a machine learner's guide to streamflow..."

       
        try:
            # enter abstract
            if talk_type in default_details.keys():
                longform = default_details[talk_type]
                longline = longform 
            else:
                if np.isnan(paper_id):
                    longform = talk['Bio'].to_numpy()[0]
                else:
                    if paper_id in abs_ids:
                        # check to see if camera ready is available

                        paper_id = int(paper_id)
                        st_with = 'papers/{}'.format(paper_id)
                        for x in cam_readys:
                            if x.startswith(st_with):
                                if 'Supplement.pdf' not in x:
                                    target_link = 'papers/ai4earth_neurips_2020_%02d.pdf' %paper_id
                                    shutil.copy2(x, target_link)
                                    title = '<a href="{}">{}</a>'.format(os.path.join(sitename,target_link), title)
                                #print(title)
                        # get the abstract
                        longform = abstracts[abstracts['Paper ID'] == paper_id]['Abstract'].to_numpy()[0]

            if type(talk_type) == str:
                video_link =  talk['Video'].to_numpy()[0]
                if type(video_link) == str:
                    talk_type = '<a href="{}">{}</a>'.format(video_link.strip(), talk_type.strip())
            author = talk['Authors'].to_numpy()[0].replace('()', '')

            link = talk['Link'].to_numpy()[0]

            if type(link) == str:
                author = '<a href="{}">{}</a>'.format(link.strip(), author.strip())

            if talk_type in ['Keynote', 'Session Keynote'] :
                #if 'Elizabeth A Barnes' in author:
                a = author.split(';')[0]
                #    panelists.append(a)
                #else:
                panelists.append(a)
            
            # split long abstracts/bios in to visible and "more" after 2 sentences
            # hacky 
            if type(longform) != type(''):
                longform = ''
            spl_str = longform.strip().split('. ')
            brk =  2
            if len(spl_str) > brk:
                st = '. '.join(spl_str[:brk]) + '.'
                en = '. '.join(spl_str[brk:]) 
                # something about Deepfish messes up the html summary function 
                if 'sensors' == session.lower():
                    longline = longform.strip() 
                else:
                #longline = """<p style="display:inline";>{}<details style="display:inline;"closed><summary>More</summary>{}</details></p>""".format(st, en)
                    longline = """{}<details style="display:inline;"closed><summary>More</summary>{}</details>""".format(st, en)
            else:
                longline = longform

            if talk_type == 'Discussion':
                if len(panelists):
                    longline += ' Discussion panelists include: ' + ' and '.join(panelists) 
                if session == 'People-Earth':
                    longline = ' Discussion panelists include: ' + ' and '.join(panelists) 
            line = """<tr>
                      <td style="text-align:center">{}</td>
                      <td style="text-align:center">{}</td>
                      <td style="text-align:center">{}</td>
                      <td style="text-align:center">{}</td>
                      <td style="text-align:center">{}</td>
                      <td style="text-align:left">{}</td>
                      </tr>""".format(ind, talk_time, talk_type,
                                 title, 
                                 author, longline)

       
            #if type(paper_id) == int:
            #     if int(paper_id) == 18:
            #         embed()

            fo.write(line)

        except Exception as e: 
            print(e)
            embed()
    #print(panelists)
    fo.write("</table>\n")
    fo.write("</html>\n\n")
    session_jumps = ['[{}](#{})'.format(s, s.lower()) for s in sessions if s not in ['Welcome', 'Closing']]
    fo.write('### Jump to: [Overview](#overview-schedule) - {}\n\n'.format('  -  '.join(session_jumps)))
fo.close()



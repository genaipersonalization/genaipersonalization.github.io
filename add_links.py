from glob import glob
import pandas as pd
from IPython import embed
import os
import shutil
import numpy as np
sitename = 'https://domaingen.github.io'

write_file = open('accepted.md', 'w')

paper_files = glob('papers/*.pdf')
poster_files = glob('posters/*.png')

poster_dict = {}
paper_dict = {}
for pp in paper_files:
    paper_dict[os.path.split(pp)[1].split('\\')[0]] = pp
for pp in poster_files:
    poster_dict[os.path.split(pp)[1].split('_')[0]] = pp
input_page = 'index.html'
camera_ready_file = 'camera_ready.csv'
poster_file = 'posters.csv'
crdf = pd.read_csv(camera_ready_file)
crdf['Status'] = 'Accept paper'
pdf = pd.read_csv(poster_file)
crdf = crdf.append(pdf)
crdf.index = np.arange(crdf.shape[0])
for ind in crdf.index:
    ff = crdf.loc[ind]
    has_pp = False; has_paper = False; has_poster = False
    if 'Accept' in ff['Status']:
        pid = str(ff['Paper ID'])
        paper_title = '**%s**'%ff['Paper Title']
        authors = ff['Author Names'].replace('*','')
        if ff['Status'] == 'Accept poster':
            first_author = authors.split(',')[0]
        else:
            first_author = authors.split('(')[0].strip().split(' ')[-1]
 
        if pid in paper_dict and ff['Status'] == 'Accept paper':
            has_pp = True
            has_paper = True
            target_path = 'camera_ready/%02d.pdf' %int(pid)
            target_link = sitename + target_path
            shutil.copy2(paper_dict[pid], target_path)
            paper = '**[paper]({})**   '.format(target_link)
        if first_author in poster_dict:
            has_pp = True
            has_poster = True
            poster =  '    **[poster]({})**'.format(sitename + poster_dict[first_author])
        if has_pp:
            write_file.write(paper_title + '  \n')
            write_file.write(authors + '  \n')
            if has_paper: 
                write_file.write(paper)
            if has_poster:
                write_file.write(poster)
            write_file.write('  \n\n')



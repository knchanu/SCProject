from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
import seaborn as sns; sns.set(style='white')
from datetime import datetime
import numpy as np
import pandas as pd
import json
import os
import re

with open(f'macrotime/pval.txt', 'w') as f:
    f.write('chi2test p-values\n')

paths = [
    '/Users/anthonysicilia/Desktop/SCProject/comments/orlando_start=2016-06-12-00:00:00_end=2016-07-12-00:00:00_ep=comment.json',
    '/Users/anthonysicilia/Desktop/SCProject/comments/lasvegas_start=2017-10-01-00:00:00_end=2017-11-01-00:00:00_ep=comment.json',    
    '/Users/anthonysicilia/Desktop/SCProject/comments/pittsburgh_start=2018-10-27-00:00:00_end=2018-11-27-00:00:00_ep=comment.json',
    '/Users/anthonysicilia/Desktop/SCProject/comments/elpaso_start=2019-08-03-00:00:00_end=2019-09-03-00:00:00_ep=comment.json'
    ]
refs = [
    # year, month, day[, hour[, minute
    (2016, 6, 12, 2, 2),
    (2017, 10, 1, 12 + 10, 5),
    (2018, 10, 27, 9, 54),
    (2019, 8, 3, 10, 39)
    ]

def time_class(time, ref):
    time = datetime.fromtimestamp(time)
    return time.year

time = dict()

for comment_path, ref in zip(paths, refs):

    save_path = comment_path.split('comments/')[1]
    save_path = save_path.split('=')[1].split('-')[0] + ' ' + save_path.split('_')[0]

    with open(comment_path) as f:
            
            try:
                x = json.load(f)
            except:
                print('Error Loading File.')
                exit()
            try:
                x = x['comments']
            except:
                print('Expected "comment" field. Field not found.')
                exit()
            
            for comment in x:
                time[comment['id']] = save_path

clusters = pd.read_csv('labels/clusters.txt')
clusters['time'] = clusters['reddit_id'].apply(lambda id_: 
    time[id_] if id_ in time else None)
clusters = clusters[~clusters['time'].isnull()]
clusters['count'] = 1.0
df = clusters.pivot_table(
    index='time', columns='cluster', 
    values='count', aggfunc=sum)
chi2, p, dof, expected = chi2_contingency(df.values)
fig, ax = plt.subplots(figsize=(20, 10))
for i in range(df.values.shape[0]):
    df.values[i] = df.values[i] / df.values[i].sum()
sns.heatmap(df, ax=ax, cmap='Blues')
plt.title(f'macrotime (across cities)')
plt.savefig(f'macrotime/viz')
with open(f'macrotime/pval.txt', 'a') as f:
    f.write(f'p-value: {p}\n')


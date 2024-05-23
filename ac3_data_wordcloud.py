#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 2024

@author: Matthias Buschmann
"""

import datetime as dt
import numpy as np
from PIL import Image

from sickle import Sickle
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# to be filled with dataset titles
titles = []

# read in image to create mask from
mask = np.array(Image.open('ellipse_mask.png'))

# define community and project id
zenodo_community = 'crc172-ac3'
pangaea_project_id = '4230'

# harvest zenodo metadata
sickle = Sickle('https://zenodo.org/oai2d')
records = sickle.ListRecords(metadataPrefix='oai_dc', set='user-'+zenodo_community)

for i, record in enumerate(records):
    try:
        titles.append(record.metadata['title'][0])
    except AttributeError as e:
        print(i, e)

# harvest pangaea metadata
sickle = Sickle('http://ws.pangaea.de/oai/provider')
records = sickle.ListRecords(metadataPrefix='oai_dc', set='project'+pangaea_project_id)
for i, record in enumerate(records):
    try:
        titles.append(record.metadata['title'][0])
    except AttributeError as e:
        print(i, e)

print(len(titles), 'titles found!')


# combine titles to one huge string
titles_combined = ''
for t in titles:
    #t = t.replace('something', 'with something else')
    titles_combined+=' '+t


# possibly define stop words
stopwords = set(STOPWORDS)
#stopwords.add('some word not to be used')


# generate wordcloud
wordcloud = WordCloud(mask=mask, 
                      collocations=True, 
                      stopwords=stopwords, 
                      max_words=100, 
                      collocation_threshold=20, 
                      background_color=None, 
                      max_font_size=60, 
                      relative_scaling=0.2, 
                      contour_width=0, 
                      mode='RGBA',
                      )

wordcloud = wordcloud.generate(titles_combined)

fig, ax = plt.subplots(1)
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
fig.savefig('wordcloud_ellipse_'+dt.datetime.now().strftime('%Y%m%d')+'.png', dpi=300, transparent=False)

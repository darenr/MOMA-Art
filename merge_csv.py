import unicodecsv
import sys
import codecs
import requests
import os
import time
from textblob import TextBlob
import re
import fractions


results = []

def enrich(m):
  r = re.search(r'([0-9 /]+)\s+x\s([0-9 /]+)["]*\s.*$', m['Dimensions'])
  if r:
    x = sum(map(fractions.Fraction, r.group(1).split()))
    y = sum(map(fractions.Fraction, r.group(2).split()) )
    print float(x), float(y)
    

with open('Artworks.csv', 'rb') as in_csv:
  for m in unicodecsv.DictReader(in_csv, encoding='utf-8'):
    url = m['URL']
    oid = m['ObjectID']

    # augment with text processing
    enrich(m)

    # merge scraped extra text
    fname = os.path.join('extras', oid + '.txt')
    if os.path.isfile(fname):
      with open(fname) as f:
        m['ExtraText'] = unicode(f.read().replace('\n', ' ').replace('\r', ''), 'utf-8')
    results.append(m)

with open('MergedArtworks.csv', 'wb') as out_csv:
  wr = unicodecsv.DictWriter(out_csv, 
        encoding='utf-8', 
        quoting=unicodecsv.QUOTE_ALL, 
        fieldnames = results[0].keys())
  wr.writeheader()
  for row in results:
    wr.writerow(row)

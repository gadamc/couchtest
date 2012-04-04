#!/usr/bin/env python                                                          
from couchdbkit import Server, Database
import datetime, copy, time


def getSeconds(td):
  return (td.microseconds + (td.seconds + td.days * 24. * 3600.) * 10.**6) /10.**6

s = Server('http://localhost:5001')
db = s['datadb2']

doc = db['run_ll20f003_011_kdatascript']
del doc['_id']
del doc['_rev']

sourcedocs = []
simpledoc = {'foo':'bar'}
#sourcedocs.append(simpledoc)
sourcedocs.append(doc)

numDocs = [10, 50, 100, 500, 1000, 2000, 5000]

results = []
for doc in sourcedocs:
  if doc.has_key('foo'):
    print doc
  else: print 'run_ll20f003_011_kdatascript'
  print 'measuring time it takes to transfer'
  print 'num, totalseconds'
  try:
    del doc['_id']
    del doc['_rev']
  except: pass
  
  for num in numDocs:
    results = []
    for ii in range(6):
      time.sleep(4)
      try:
        start = datetime.datetime.now()
        for i in range(num):
          db.save_doc(doc)

        stop = datetime.datetime.now()
        results.append( str(getSeconds(stop - start)) )
      except:
        print num, ',', ','.join(results)
        raise
    print num, ',', ','.join(results)
      

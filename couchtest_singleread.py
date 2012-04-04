#!/usr/bin/env python                                                          
from couchdbkit import Server, Database
import datetime, copy, time


def getSeconds(td):
  return (td.microseconds + (td.seconds + td.days * 24. * 3600.) * 10.**6) /10.**6

s = Server('http://localhost:5001')
db = s['datadb2']
docnames = []
docnames.append('run_ll20f003_011_kdatascript')
docnames.append('superfoobar')
doc = {}
doc['foo'] = 'bar'
doc['_id'] =  docnames[1]
try:
  db.save_doc(doc)
except:
  db.delete_doc(doc['_id'])
  db.save_doc(doc)
  
numDocs = [10, 50, 100, 500, 1000,5000,10000, 50000]
#numDocs = [10]

results = []

for docname in docnames:
  print docname
  
  for num in numDocs:
    results = []
    for ii in range(6):
      time.sleep(2)
      try:
        start = datetime.datetime.now()
        for i in range(num):
          ddoc = db[docname]

        stop = datetime.datetime.now()
        results.append( str(getSeconds(stop - start)) )
      except:
        print num, ',', ','.join(results)
        raise
    print num, ',', ','.join(results)
      

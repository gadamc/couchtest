#!/usr/bin/env python

from couchdbkit import Server, Database
import datetime, copy, time

s = Server('http://localhost:5001')
db = s['datadb2']
#doc = db['run_ma22a000_000_kdatascript']
doc = db['run_ll20f003_011_kdatascript']

del doc['_id']
del doc['_rev']

sourcedocs = []
simpledoc = {'foo':'bar'}
sourcedocs.append(simpledoc)
sourcedocs.append(doc)


#numDocs = [100,200,500,1000,1100,1200,1300,1400, 1500, 1600,1700, 1800, 1900, 2000, 4000, 8000, 10000, 15000, 30000, 100000, 300000, 500000]

numDocs = [10, 50, 100, 500, 1000, 1500, 5000, 10000, 20000, 50000, 100000]

#numDocs = [300000, 500000, 1000000]


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
    try: 
      for ii in range(6):
        docs = []
        #print 'getting uuid'
        time.sleep(2)
        for i in range(num):
          newdoc = copy.deepcopy(doc)
          newdoc['_id'] = s.next_uuid(num)
          #print newdoc['_id']
          docs.append(newdoc)

        dumbdoc = db['run_ll20f003_011_kdatascript']
        time.sleep(4)
        start = datetime.datetime.now()
        #print start
        db.bulk_save(docs)
        del docs
        stop = datetime.datetime.now()
        td = stop - start
        totalsec = (td.microseconds + (td.seconds + td.days * 24. * 3600.) * 10.**6) /10.**6
    #print num, 'file puts in ', totalsec, ' seconds', float(num)/float(totalsec), 'docs per second' 
        results.append(str(totalsec))
    except:
      print num, ',', ','.join(results)
      raise
    print num, ',', ','.join(results)

#!/usr/bin/env python                                                          
from couchdbkit import Server, Database
import datetime, copy, time, sys


def getSeconds(td):
  return (td.microseconds + (td.seconds + td.days * 24. * 3600.) * 10.**6) /10.**6


'''
need to create two views in your database for this to work.
proc/proc0:

function(doc) {
    if(doc.type == "daqdocument" && doc.status == "closed" && !doc.proc0 && doc.Intitule != "Edelweiss 2, run 15"){
	emit( doc.run_name, 1);
    }
}

proc/foo

function(doc) {
    if(doc.foo && doc.status == "closed"){
	emit( doc.foo, 1);
    }
}

i would do it here automatically, but i don't immediately know how and i don't want to figure it out

'''

s = Server('http://localhost:5001')
db = s['datadb2']  #DON'T USE A REAL DATABASE! CREATE A NEW ONE FOR TESTING, YO! 

doc = db['run_ll20f003_011_kdatascript']
del doc['_id']
del doc['_rev']
doc['status'] = 'closed'
try:
  del doc['proc0']
except: pass
try:
  del doc['proc1']
except: pass
try:
  del doc['proc2']
except: pass

vr = db.view('proc/foo', reduce=False)
for row in vr:
  db.delete_doc(row['id'])

vr = db.view('proc/proc0', reduce=False)
for row in vr:
  db.delete_doc(row['id'])
    

sourcedocs = []
simpledoc = {'foo':'bar', 'status':'closed'}
sourcedocs.append(simpledoc)
sourcedocs.append(doc)

#numDocs = [10, 50, 100, 500, 1000, 2000, 5000]
numDocs = [1, 5, 10, 50, 100, 500, 1000]

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
        totlSec = datetime.timedelta()
        for i in range(num):
          #savedoc = copy.deepcopy(doc)  #refresh the doc every time!
          try:
            del doc['_id']
            del doc['_rev']
          except: pass
          
          start = datetime.datetime.now()
          #db.save_doc(savedoc)
          db.save_doc(doc)
          if doc.has_key('foo'):
            vr = db.view('proc/foo', reduce=False, include_docs=True)
          else:
            vr = db.view('proc/proc0', reduce=False, include_docs = True)
          
          upDoc = vr.first()['doc']
          upDoc['status'] = 'good'
          upDoc['proc0'] = 'test proc done'
          db.save_doc(upDoc)
          stop = datetime.datetime.now()
          totlSec += stop-start
          
        results.append( str(getSeconds(totlSec)) )
      except:
        print num, ',', ','.join(results)
        raise
    print num, ',', ','.join(results)
      

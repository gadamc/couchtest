#!/usr/bin/env python                                                          
from couchdbkit import Server, Database
import datetime, copy

s = Server('http://localhost:5984')
db = s['datadb2']


start = datetime.datetime.now()
print start

for i in range(1000):
  doc = db['run_mc23e003_000_kdatascript']
  if i % 2 == 0: doc['status'] = 'good'
  else:doc['status'] ='testing'
  db.save_doc(doc)

stop = datetime.datetime.now()

print '1000 file puts:', stop - start

doc = db['run_mc23e003_000_kdatascript']
doc['status'] = 'good'
db.save_doc(doc)

import os
import sys 
import sqlite3
import hashlib
import datetime
import csv
from urlparse import urlparse
from ToolMappingClass import ToolMapping
from CSVHandlerClass import *

class DROIDLoader:

   basedb = ''
   hashtype = ''
   BOM = False
         
   def __init__(self, basedb, BOM=False):
      self.basedb = basedb
      self.BOM = BOM
   
   def createDROIDTable(self, cursor, csvcolumnheaders):
      # turn csv headers list into a csv string, write query, create table

      self.csvcolumncount = len(csvcolumnheaders)
      columns = ""
      for header in csvcolumnheaders:
         if header == "URI":
            columns = columns + header + ", " + "URI_SCHEME, "
            self.csvcolumncount+=1
         elif header == "FILE_PATH":
            columns = columns + header + ", " + "DIR_NAME, "
            self.csvcolumncount+=1
         elif "_HASH" in header:    #regex alternative: ^([[:alnum:]]*)(_HASH)$
            self.basedb.sethashtype(header.split('_', 1)[0])
            columns = columns + "HASH" + ", "
         elif header == "LAST_MODIFIED":
            columns = columns + header + " TIMESTAMP" + ","
            columns = columns + "YEAR INTEGER" + ","
         else:
            #sys.stderr.write(header + "\n")
            columns = columns + header + ", "

      cursor.execute("CREATE TABLE droid (" + columns[:-2] + ")")
      return True

   def insertfiledbstring(self, keys, values):
      insert = "INSERT INTO " + self.basedb.FILEDATATABLE
      return insert + "(" + keys.strip(", ") + ") VALUES (" + values.strip(", ") + ");"

   def insertiddbstring(self, keys, values):
      insert = "INSERT INTO " + self.basedb.IDTABLE
      return insert + "(" + keys.strip(", ") + ") VALUES (" + values.strip(", ") + ");"

   def droidDBSetup(self, droidcsv, cursor):

      if droidcsv != False:
         droidcsvhandler = droidCSVHandler()
         droidlist = droidcsvhandler.readDROIDCSV(droidcsv, self.BOM)

      droidlist = droidcsvhandler.addurischeme(droidlist)
      droidlist = droidcsvhandler.addYear(droidlist)

      for x in droidlist:
         filekeystring = ''
         filevaluestring = ''
         idkeystring = ''
         idvaluestring = ''
         for key, value in x.items():
            if key in ToolMapping.FILE_MAP:
               filekeystring = filekeystring + ToolMapping.FILE_MAP[key] + ", "
               filevaluestring = filevaluestring + "'" + value + "', "
            if key in ToolMapping.DROID_ID_MAP:
               idkeystring = idkeystring + ToolMapping.DROID_ID_MAP[key] + ", "
               idvaluestring = idvaluestring + "'" + value + "', "
   
         cursor.execute(self.insertfiledbstring(filekeystring, filevaluestring))
         cursor.execute(self.insertiddbstring(idkeystring, idvaluestring))



   def _droidDBSetup(self, droidcsv, cursor):

      with open(droidcsv, 'rb') as csvfile:
      
         droidreader = csv.reader(csvfile)

         for row in droidreader:
            #if droidreader.line_num == 1:		# not zero-based index
            #   tablequery = self.createDROIDTable(cursor, row)
            #else:
            rowstr = ""	
            for i,item in enumerate(row[0:18-1]):

               if i != 18:  #avoid overrun of columns when multi-id occurs
                  
                  if item == "":
                     rowstr = rowstr + ',"no value"'
                  else:
                     rowstr = rowstr + ',"' + item + '"'
                                    
                     '''if i == self.URI_COL:
                        url = item
                        rowstr = rowstr + ',"' + urlparse(url).scheme + '"'

                     if i == self.PATH_COL:
                        dir = item
                        rowstr = rowstr + ',"' + os.path.dirname(item) + '"'		

                     if i == self.DATE_COL:
                        if item is not '':
                           datestring = item
                           #split at '+' if timezone is there, we're only interested in year
                           dt = datetime.datetime.strptime(datestring.split('+', 1)[0], '%Y-%m-%dT%H:%M:%S')
                           rowstr = rowstr + ',"' + str(dt.year) + '"'
                        else:
                           rowstr = rowstr + ',"' + "no value" + '"'''
               
               #print rowstr
               #cursor.execute("INSERT INTO droid VALUES (" + rowstr.lstrip(',') + ")")

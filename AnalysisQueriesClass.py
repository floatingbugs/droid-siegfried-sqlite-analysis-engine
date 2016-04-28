﻿class AnalysisQueries:
   
   SELECT_FILENAMES = "SELECT FILEDATA.NAME FROM FILEDATA"
   SELECT_DIRNAMES = "SELECT DISTINCT FILEDATA.DIR_NAME FROM FILEDATA"
   
   SELECT_HASH = "SELECT DBMD.HASH_TYPE FROM DBMD"
   SELECT_TOOL = "SELECT DBMD.TOOL_TYPE FROM DBMD"
   
   SELECT_COLLECTION_SIZE = "SELECT SUM(FILEDATA.SIZE) FROM FILEDATA"
   SELECT_COUNT_FILES = "SELECT COUNT(FILEDATA.FILE_ID) FROM FILEDATA WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')"
   
   SELECT_COUNT_CONTAINERS = "SELECT COUNT(FILEDATA.FILE_ID) FROM FILEDATA WHERE FILEDATA.TYPE='Container'"
   SELECT_CONTAINER_TYPES = "SELECT DISTINCT FILEDATA.URI_SCHEME FROM FILEDATA WHERE (FILEDATA.TYPE='File' AND FILEDATA.URI_SCHEME!='file')"
   SELECT_COUNT_FILES_IN_CONTAINERS = "SELECT COUNT(FILEDATA.FILE_ID) FROM FILEDATA WHERE (FILEDATA.URI_SCHEME!='file') AND (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')"

   SELECT_COUNT_ZERO_BYTE_FILES = "SELECT COUNT(FILEDATA.SIZE) FROM FILEDATA WHERE (FILEDATA.TYPE!='Folder') AND (FILEDATA.SIZE='0')"
   SELECT_ZERO_BYTE_FILEPATHS = "SELECT FILEDATA.FILE_PATH FROM FILEDATA WHERE FILEDATA.TYPE='File' AND FILEDATA.SIZE='0'"

   SELECT_COUNT_FOLDERS = "SELECT COUNT(FILEDATA.FILE_ID) FROM FILEDATA WHERE FILEDATA.TYPE='Folder'"
   
   SELECT_COUNT_UNIQUE_FILENAMES = "SELECT COUNT(DISTINCT FILEDATA.NAME) FROM FILEDATA WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')"
   SELECT_COUNT_UNIQUE_DIRNAMES =  "SELECT COUNT(DISTINCT FILEDATA.DIR_NAME) FROM FILEDATA"
   
   SELECT_COUNT_NAMESPACES = 'SELECT COUNT(NSDATA.NS_ID) FROM NSDATA'
   
   SELECT_COUNT_ID_METHODS = """SELECT IDRESULTS.FILE_ID, IDDATA.METHOD as METHOD
                              FROM IDRESULTS
                              JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID"""

   SELECT_COUNT_EXT_MISMATCHES = """SELECT COUNT(distinct(IDRESULTS.FILE_ID))
                                       FROM IDRESULTS
                                       JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                       WHERE IDDATA.EXTENSION_MISMATCH='True'"""                                          

   #TODO: Currency is PUID, what do we do for Tika and Freedesktop and others?
   SELECT_COUNT_FORMAT_COUNT = """SELECT COUNT(DISTINCT IDDATA.ID)
                                    FROM IDRESULTS
                                    JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID
                                    JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                    WHERE (NSDATA.NS_NAME='pronom')
                                    AND (IDDATA.METHOD='Signature' OR IDDATA.METHOD='Container')"""

   SELECT_COUNT_OTHER_FORMAT_COUNT = """SELECT COUNT(DISTINCT IDDATA.ID)
                                       FROM IDRESULTS
                                       JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID
                                       JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                       WHERE (NSDATA.NS_NAME!='pronom')
                                       AND (IDDATA.METHOD='Signature' OR IDDATA.METHOD='Container')"""

   #PRONOM and OTHERS Text identifiers as one result
   SELECT_COUNT_TEXT_IDENTIFIERS = """SELECT count(DISTINCT IDMETHOD)
                                       FROM (SELECT IDRESULTS.FILE_ID, IDDATA.ID as IDMETHOD
                                       FROM IDRESULTS
                                       JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID
                                       JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                       AND (IDDATA.METHOD='Text'))"""

   #PRONOM and OTHERS Filename identifiers as one result
   SELECT_COUNT_FILENAME_IDENTIFIERS = """SELECT COUNT(DISTINCT IDMETHOD)
                                             FROM (SELECT IDRESULTS.FILE_ID, IDDATA.ID as IDMETHOD
                                             FROM IDRESULTS
                                             JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID
                                             JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                             AND (IDDATA.METHOD='Filename'))"""

   SELECT_COUNT_EXTENSION_RANGE = """SELECT COUNT(DISTINCT FILEDATA.EXT) 
                                       FROM FILEDATA  
                                       WHERE FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container'"""

   SELECT_METHOD_FREQUENCY_COUNT = """SELECT IDDATA.METHOD, COUNT(*) AS total 
                                       FROM IDRESULTS  
                                       JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                                       JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID                                          
                                       WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container') 
                                       GROUP BY IDDATA.METHOD ORDER BY TOTAL DESC"""	

   #select the gamut of MIMEs in the accession/extract, not counts
   SELECT_MIME_RANGE = """SELECT DISTINCT IDDATA.MIME_TYPE AS total 
                                       FROM IDRESULTS 
                                       JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID                                      
                                       GROUP BY IDDATA.MIME_TYPE ORDER BY TOTAL DESC"""

   SELECT_DISTINCT_BINARY_MATCH_NAMES = """SELECT DISTINCT IDDATA.ID, NSDATA.NS_NAME, IDDATA.FORMAT_NAME, IDDATA.FORMAT_VERSION
                                             FROM IDDATA
                                             JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID
                                             WHERE (IDDATA.METHOD='Signature' OR IDDATA.METHOD='Container')
                                             ORDER BY NSDATA.NS_NAME"""

   SELECT_BINARY_MATCH_COUNT = """SELECT NSDATA.NS_NAME, IDDATA.ID, COUNT(IDDATA.ID) as TOTAL
                                    FROM IDRESULTS
                                    JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID
                                    JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                    WHERE (IDDATA.METHOD='Signature' OR IDDATA.METHOD='Container')
                                    GROUP BY IDDATA.ID ORDER BY NSDATA.NS_NAME, TOTAL DESC"""

   SELECT_YEAR_FREQUENCY_COUNT = """SELECT FILEDATA.YEAR, COUNT(FILEDATA.YEAR) AS total 
                                       FROM FILEDATA 
                                       WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container') 
                                       GROUP BY FILEDATA.YEAR ORDER BY TOTAL DESC"""


   #TODO: THIS STAT NEEDS REVISITING IN LIGHT OF SIEGFRIED
   #MULTIPLE IDS WILL BE REFLECTED USING MULTIPLE NAMESPACE PLACES - HOW TO REPORT ON?
   SELECT_PUIDS_EXTENSION_ONLY = """SELECT DISTINCT IDDATA.ID, IDDATA.FORMAT_NAME 
                                       FROM IDDATA 
                                       WHERE (IDDATA.METHOD='Extension')"""
   
   SELECT_ALL_UNIQUE_EXTENSIONS = """SELECT DISTINCT FILEDATA.EXT 
                                       FROM FILEDATA 
                                       WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')"""

   SELECT_COUNT_EXTENSION_FREQUENCY = """SELECT FILEDATA.EXT, COUNT(*) AS total 
                                             FROM FILEDATA
                                             WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container') 
                                             GROUP BY FILEDATA.EXT ORDER BY TOTAL DESC"""

   SELECT_EXTENSION_MISMATCHES = """SELECT FILEDATA.FILE_PATH 
                                             FROM IDRESULTS 
                                             JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                                             JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID                                              
                                             WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container') 
                                             AND (IDDATA.EXTENSION_MISMATCH=1)"""

   #MULTIPLE ID FOR FILES GREATER THAN ZERO BYTES
   SELECT_MULTIPLE_ID_PATHS = """SELECT FILEDATA.FILE_PATH 
                                 FROM IDRESULTS 
                                 JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                                 JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID                                      
                                 WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container') 
                                 AND (IDDATA.FORMAT_COUNT > 1) 
                                 AND (FILEDATA.SIZE > 0)"""

   SELECT_COUNT_DUPLICATE_CHECKSUMS = """SELECT FILEDATA.HASH, COUNT(*) AS TOTAL
                                          FROM FILEDATA
                                          WHERE FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container'
                                          GROUP BY FILEDATA.HASH
                                          HAVING TOTAL > 1
                                          ORDER BY TOTAL DESC"""

   SELECT_ZERO_ID_FILES = """SELECT FILEDATA.FILE_PATH
                                 FROM IDRESULTS
                                 JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                                 JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID                                   
                                 WHERE IDDATA.METHOD='None' 
                                 AND (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')"""

   def count_multiple_ids(self, nscount):
      multi = """SELECT count(FREQUENCY) from(SELECT FILE_ID, COUNT(FILE_ID) AS FREQUENCY
                  FROM IDRESULTS
                  GROUP BY FILE_ID
                  ORDER BY
                  COUNT(FILE_ID) DESC)
                  WHERE FREQUENCY > """
      multi = multi + str(nscount)
      return multi

   def list_duplicate_paths(self, checksum):
      return "SELECT FILE_PATH FROM FILEDATA WHERE FILEDATA.HASH='" + checksum + "'ORDER BY FILEDATA.FILE_PATH"

   def count_id_instances(self, id):
      return "SELECT COUNT(*) AS total FROM IDDATA WHERE (IDDATA.ID='" + id + "')"

   def search_id_instance_filepaths(self, id):
      query_part1 = """SELECT FILEDATA.FILE_PATH 
                        FROM IDRESULTS 
                        JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                        JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID  
                        WHERE IDDATA.ID='""" 
      
      query_part2 = id + "' ORDER BY FILEDATA.FILE_PATH DESC"      
      return query_part1 + query_part2

   def extension_only_identification(self, idlist, method):
      list = 'AND '
      for i in idlist:
         where = "IDRESULTS.FILE_ID=" + str(i) + " OR "
         list = list + where
      list = list.rstrip(' OR ')            
      SELECT_EXT_ONLY_FREQUENCY = """SELECT NSDATA.NS_NAME, IDDATA.ID
                                       FROM IDRESULTS
                                       JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID
                                       JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                       WHERE IDDATA.METHOD="""
                                       
      SELECT_EXT_ONLY_FREQUENCY = SELECT_EXT_ONLY_FREQUENCY + "'" + method + "'"    #which method?         
      return SELECT_EXT_ONLY_FREQUENCY + "\n" + list                                     

   #ERRORS, TODO: Place somewhere else?
   ERROR_NOHASH = "Unable to detect duplicates: No HASH algorithm used by identification tool."

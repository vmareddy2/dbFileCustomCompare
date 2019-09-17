import argparse
import csv
import sys

def parse_args() -> (str,str) :
  parser = argparse.ArgumentParser(description='Process two csv files, based on column matches and show columns that are different in data')
  parser.add_argument('--fileToCompare', dest='fileToCompare')
  parser.add_argument('--fileToCompareWith', dest='fileToCompareWith')
  args = parser.parse_args()
  return (args.fileToCompare, args.fileToCompareWith)

def get_dict(file: str):
  colName = []
  dict_wid = {}
  dict_sfid = {}

  with open(file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
      if line_count == 0:
        colName = row
        line_count = line_count+1
      else:
        # populate dict_wid
        tempRow = row.copy()
        wid = tempRow.pop(0)
        if(wid!=""):
          if wid in dict_wid.keys():
            dict_wid[wid] = dict_wid[wid]+[tempRow]
          else:
            dict_wid[wid]=[tempRow]
        else:
          print("worker id is empty in row"+str(line_count))

        #populate dict_sfid
        tempRow2 = row.copy()
        sid = tempRow2.pop(1)
        if(sid!=""):
          if sid in dict_sfid.keys():
            dict_sfid[sid] = dict_sfid[sid]+[tempRow2]
          else:
            dict_sfid[sid]=[tempRow2]
        else:
          print("supportforce id is empty in row"+str(line_count))

        line_count = line_count + 1


    return (colName, dict_wid, dict_sfid)


def compareAndPrintColumns(colNames, dict_wid, dict_sfid, file):
  with open(file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
      if line_count == 0:
        if colNames != row:
          print("ERROR: Column Names in both files are not equal")
          print(row)
          print(colNames)
          sys.exit(-1)
        line_count = line_count + 1
      else:
        line_count = line_count + 1

        tempRow = row.copy()
        ig_wid = tempRow.pop(0)
        tempCol = colNames.copy()
        tempCol.pop(0)
        #match on worker id
        if( ig_wid != "" and ig_wid in dict_wid.keys() ):
          for row2 in dict_wid[ig_wid]:
            if tempRow != row2:
              print(ig_wid,end=': ')
              for i in range(0,len(row2)):
                if tempRow[i] != row2[i]:
                  print(tempCol[i],end=' ')
          print('\n')

  print(''''---- done matching on worker---''')

  with open(file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
      if line_count == 0:
        if colNames != row:
          print("ERROR: Column Names in both files are not equal")
          print(row)
          print(colNames)
          sys.exit(-1)
        line_count = line_count + 1
      else:
        line_count = line_count + 1


        tempRow2 = row.copy()
        ig_sid = tempRow2.pop(1)
        tempCol2 = colNames.copy()
        tempCol2.pop(1)
        #match on supportforce id
        if( ig_sid != "" and ig_sid in dict_sfid.keys() ):
          for row3 in dict_sfid[ig_sid]:
            if tempRow2 != row3:
              print(ig_sid,end=': ')
              for i in range(0,len(row3)):
                if tempRow2[i] != row3[i]:
                  print(tempCol2[i],end=' ')
          print('\n')


def main():
  (fileToCompare, fileToComapreWith) = parse_args()
  (columns, dict_key_workerid, dict_key_supportforceid) = get_dict(fileToComapreWith)
  compareAndPrintColumns(columns, dict_key_workerid, dict_key_supportforceid, fileToCompare)


if __name__ == "__main__":
  main()

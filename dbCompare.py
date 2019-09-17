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
        if(row[0]!=""):
          if row[0] in dict_wid.keys():
            dict_wid[row[0]] = dict_wid[row[0]]+[row[1:]]
          else:
            dict_wid[row[0]]=[row[1:]]
        else:
          print("worker id is empty in row"+str(line_count))

        #populate dict_sfid
        if(row[6]!=""):
          if row[6] in dict_wid.keys():
            dict_sfid[row[6]] = dict_wid[row[6]]+[row[:6]]
          else:
            dict_sfid[row[6]]=[row[:6]]
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

        #match on worker id
        if( row[0] != "" and row[0] in dict_wid.keys() ):
          for row2 in dict_wid[row[0]]:
            if row[1:] != row2:
              print(row[0],end=': ')
              for i in range(0,len(row2)):
                if row[i+1] != row2[i]:
                  print(colNames[i+1],end=' ')
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

        #match on supportforce id
        if( row[6] != "" and row[6] in dict_sfid.keys() ):
          for row3 in dict_sfid[row[6]]:
            if row[:6] != row3:
              print(row[6],end=': ')
              for i in range(0,len(row3)):
                if row[i] != row3[i]:
                  print(colNames[i],end=' ')
          print('\n')


def main():
  (fileToCompare, fileToComapreWith) = parse_args()
  (columns, dict_key_workerid, dict_key_supportforceid) = get_dict(fileToComapreWith)
  compareAndPrintColumns(columns, dict_key_workerid, dict_key_supportforceid, fileToCompare)


if __name__ == "__main__":
  main()

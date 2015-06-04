import MapReduce
import sys

"""
Friend count in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: person_a
    # value: friend
    key = record[0]
    value = record[1]
    mr.emit_intermediate(key,1)

def reducer(key, list_of_values):
    # key: person
    # value: list of 1s  
    mr.emit((key, sum(list_of_values)))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

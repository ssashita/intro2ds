import MapReduce
import sys

"""
Assym Friend  in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: person_a
    # value: friend
    key = record[0]
    value = record[1]
    superkey=[key,value]
    superkey.sort()
    mr.emit_intermediate(superkey[0]+superkey[1],[key,value])

def reducer(key, list_of_values):
    # key: [personA,personB]
    # list_of_values: list [[personA,personB]] or[[personA,personB],[personB,personA]]
    if len(list_of_values) == 1:
        for el in list_of_values:
            mr.emit((el[0],el[1]))
            mr.emit((el[1],el[0]))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

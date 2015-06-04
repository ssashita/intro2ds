import MapReduce
import sys

"""
Inverted Word Index in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: DNA string identifier
    # value: DNA sequence string
    key = record[0]
    value = record[1]
    trimmedval = value[:-10]
#    print len(trimmedval)
    mr.emit_intermediate(trimmedval,None)

def reducer(key, list_of_values):
    # key: DNA string
    # value: junk
    
    mr.emit(key)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
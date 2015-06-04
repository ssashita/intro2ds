import MapReduce
import sys

"""
Inverted Word Index in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = value.split()
    wordset=set()
    for w in words:
        if w not in wordset:
            mr.emit_intermediate(w,key)
            wordset.add(w)

def reducer(key, list_of_values):
    # key: word
    # value: list of books where found    
    mr.emit((key, list_of_values))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

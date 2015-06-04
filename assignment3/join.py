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
    relation = record[0]
    key = record[1]
    mr.emit_intermediate(key,record)

def reducer(key, list_of_values):
    # key: word
    # value: list of records with tuples each of form (relation,ordernum,...)
    orders=[o for o in list_of_values if o[0]=='order']
    lineitems =[l for l in list_of_values if l[0]=='line_item']
    for el in [o+l for o in orders for l in lineitems]:
        mr.emit(el)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

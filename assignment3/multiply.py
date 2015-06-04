import MapReduce
import sys

"""
Sparse Matrix multiply in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # i,j: 
    # value:
    matrix=record[0]
    i,j = record[1:3]
    value = record[3]
    if matrix=='a':
        for k in range(5):
            mr.emit_intermediate(str(i) + " " + str(k),record)
    else:
        for k in range(5):
            mr.emit_intermediate(str(k) + " " + str(j),record)

def reducer(key, list_of_values):
    # key: i,j for the result matrix
    # value: record
    i,j=key.split()
    i=int(i)
    j=int(j)
    def i_or_j(rec):
        if rec[0]=='a':
            return 2
        else:
            return 1
    a={lv[u]:lv[3] for lv in list_of_values for u in [i_or_j(lv)] if u==2}
    b={lv[u]:lv[3] for lv in list_of_values for u in [i_or_j(lv)] if u==1}
    print i,j
    print a
    print b
    summ =0
    for k in range(5):
        a_=b_=None
        if k in a:
            a_=a[k]
        if k in b:
            b_=b[k]
        if a_ != None and b_ != None:
            summ = summ + a_*b_
    mr.emit((i,j,summ))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
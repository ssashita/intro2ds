
def mapper(record):
    # key: DNA string identifier
    # value: DNA sequence string
    key = record[0]
    value = record[1]
    trimmedval = value[:-10]
    mr.emit_intermediate(trimmedval,None)

def reducer(key, list_of_values):
    # key: DNA string
    # value: junk
    mr.emit(key)

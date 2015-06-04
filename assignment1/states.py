import sys
import json
import us_states_json
import operator

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

def get_scores(scores_file):
    afinnfile = open(scores_file)
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
    #print scores.items() # Print every (term, score) pair in the dictionary
    return scores
    #close(scores_file)

def get_english_tweet_object(line):
    obj= json.loads(line)
    #print obj
    if "created_at" in obj and "text" in obj and "lang" in obj and obj['lang']=='en':
        return obj
    return None

def lines(fp):
    print str(len(fp.readlines()))

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    
    #hw()
    #lines(sent_file)
    #lines(tweet_file)
    state_sentiment={}
    scores = get_scores(sys.argv[1])
    state_tweet_count={}
    for line in tweet_file.readlines():
        tweet = get_english_tweet_object(line)
        if tweet != None:
            s,states=get_sentiment(tweet,scores)
            for state in states:
                count =0
                if state in state_tweet_count :
                    count = state_tweet_count[state]
                state_tweet_count[state] = count + 1
                senti=0
                if state in state_sentiment:
                    senti=state_sentiment[state]                
                state_sentiment[state] = senti + s
    state_senti={k:state_sentiment[k]/float(state_tweet_count[k]) for k in state_sentiment}
    v=list(state_senti.values())
    k=list(state_senti.keys())
    print k[v.index(max(v))]
    #print k[v.index(min(v))]
    print sorted(state_senti.iteritems(),key=operator.itemgetter(1))
    #print state_tweet_count
    
def get_sentiment(tweet,scores):
    text = tweet['text']
    senti=0
    states = get_tweet_states(tweet)
    if text != None and states != None and len(states) > 0:
        words=text.split()
        for word in words:
            score =0
            if word in scores:
                score = scores[word]
                senti = senti + score
    return senti, states

def get_tweet_states(tweet):
    states=None
    if tweet["coordinates"] != None:
        states=get_states_around(tweet["coordinates"]["coordinates"])
    elif tweet["place"] != None:
        states=get_state_from_place(tweet["place"])
    elif tweet["user"] != None and tweet["user"]["location"] != None:
        states=get_state_from_user_location(tweet["user"]["location"])
    return states
    
def get_state_from_user_location(location):
    words=location.split(',')
    states = []
    for word in words:
        if word.strip() in states:
            state = word.strip()
            states.append(state)
            break
    return states
        
    
        
def get_states_around(coord):
    longi,lat=coord
    states=[]
    for st in us_states["features"]:
        xminus,yminus,xplus,yplus=st["bbox"]
        if longi >=xminus and longi <=xplus and lat >= yminus and lat <= yplus:
            states.append(st["properties"]["state"].upper())
    return states

def get_state_from_place(place):
    if place["bounding_box"] != None and place["bounding_box"]["type"]=="Polygon":
        polygons=place["bounding_box"]["coordinates"]
        xmean=0
        ymean=0
        count=0
        for poly in polygons:
            for point in poly:
                count = count +1
                xmean = xmean + point[0]
                ymean = ymean + point[1]
            xmean = xmean / float(count)
            ymean = ymean / float(count)
        if xmean >0 and ymean >0:
            return get_states_around((xmean,ymean))
        return []
  
if __name__ == '__main__':
    us_states=json.loads(us_states_json.us_states_json)
    main()








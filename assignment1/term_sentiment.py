import sys
import json

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

    
def get_sentiment(tweet,scores):
    text = tweet['text']
    senti=0
    other_terms=set()
    count=0
    if text != None:
        words=text.split()
        for word in words:
            score =0
            if word in scores:
                score = scores[word]
                senti = senti + score
                count = count +1
            else:
                other_terms.add(word)
    return senti,count,other_terms
    
def main():
    tweet_file = open(sys.argv[2])
#    hw()
#    lines(sent_file)
#    lines(tweet_file)
    scores = get_scores(sys.argv[1])
    other_terms_senti = {}
    other_terms_freq={}
    for line in tweet_file.readlines():
        tweet = get_tweet_object(line)
        if tweet != None:
            s,count,others=get_sentiment(tweet,scores)
            meansenti = 0.0
            if count>0:
                meansenti= s/ float(count)
            for term in others:
                if term not in other_terms_senti:
                    other_terms_senti[term]=0.0
                    other_terms_freq[term] = 1
                else:
                    other_terms_senti[term]= other_terms_senti[term] + meansenti
                    other_terms_freq[term] = 1 + other_terms_freq[term]
    for term in other_terms_senti:
        print term, other_terms_senti[term]/other_terms_freq[term]

def get_tweet_object(line):
    obj= json.loads(line)
    #print obj
    if "created_at" in obj and "user" in obj and "lang" in obj["user"]:
        return obj
    return None

    
def get_scores(scores_file):
    afinnfile = open(scores_file)
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
    #print scores.items() # Print every (term, score) pair in the dictionary
    return scores
    #close(scores_file)
    
if __name__ == '__main__':
    main()

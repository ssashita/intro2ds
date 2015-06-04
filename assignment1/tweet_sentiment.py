import sys
import json

def hw():
    print 'Hello, world!'

def get_scores(scores_file):
    afinnfile = open(scores_file)
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
    #print scores.items() # Print every (term, score) pair in the dictionary
    return scores
    #close(scores_file)

def get_tweet_object(line):
    obj= json.loads(line)
    #print obj
    if "created_at" in obj and "user" in obj and "lang" in obj["user"]:
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
    scores = get_scores(sys.argv[1])
    for line in tweet_file.readlines():
        tweet = get_tweet_object(line)
        if tweet != None:
            s=get_sentiment(tweet,scores)
            print s

def get_sentiment(tweet,scores):
    text = tweet['text']
    senti=0
    if text != None:
        words=text.split()
        for word in words:
            score =0
            if word in scores:
                score = scores[word]
                senti = senti + score
    return senti
    
if __name__ == '__main__':
    main()

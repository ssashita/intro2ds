import sys
import json

def get_term_count(tweet):
    text = tweet['text']
    term_counts=dict()
    total_count=0
    if text != None:
        words=text.split()
        for word in words:
            total_count = total_count +1
            if word in term_counts:
                term_counts[word] = term_counts[word] + 1
            else:
                term_counts[word] = 1
    return total_count,term_counts
    

    
def main():
    tweet_file = open(sys.argv[1])
    overall_term_counts = {}
    total_term_count=0
    for line in tweet_file.readlines():
        tweet = get_tweet_object(line)
        if tweet != None:
            count,term_counts=get_term_count(tweet)
            total_term_count = total_term_count + count
            for term in term_counts:
                if term not in overall_term_counts:
                    overall_term_counts[term]=term_counts[term]
                else:
                    otcount = overall_term_counts[term]
                    overall_term_counts[term]= otcount + term_counts[term]
    for term in overall_term_counts:
        print term, overall_term_counts[term]/float(total_term_count)

def get_tweet_object(line):
    obj= json.loads(line)
    #print obj
    if "created_at" in obj and "user" in obj and "lang" in obj["user"]:
        return obj
    return None

    
if __name__ == '__main__':
    main()

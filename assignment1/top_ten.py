import sys
import json
import operator

def get_tag_count(tweet):
    ents = tweet['entities']
    if ents != None:
        tags=ents["hashtags"]
    tag_counts=dict()
    if tags != None and len(tags) >0:
        for tag in tags:
            if tag["text"] in tag_counts:
                tag_counts[tag["text"]] = tag_counts[tag["text"]] + 1
            else:
                tag_counts[tag["text"]] = 1
    return tag_counts
    

    
def main():
    tweet_file = open(sys.argv[1])
    overall_tag_counts = {}
    for line in tweet_file.readlines():
        #print line
        tweet = get_tweet_object(line)
        if tweet != None:
            tag_counts=get_tag_count(tweet)
            for tag in tag_counts:
                if tag not in overall_tag_counts:
                    overall_tag_counts[tag]=tag_counts[tag]
                else:
                    otcount = overall_tag_counts[tag]
                    overall_tag_counts[tag]= otcount + tag_counts[tag]
    sortedlist = sorted(overall_tag_counts.iteritems(), key=operator.itemgetter(1), reverse=True)
    for tup in sortedlist[:10]:
        print tup[0], tup[1]

def get_tweet_object(line):
    obj= json.loads(line)
    #print obj
    if "created_at" in obj and "user" in obj and "lang" in obj and obj["lang"]=='en':
        return obj
    return None

    
if __name__ == '__main__':
    main()

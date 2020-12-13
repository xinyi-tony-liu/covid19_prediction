from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from textblob import TextBlob
import sys
import requests

outputPath = sys.argv[1]

def mapToKeyValPair(line):
    countryCode = line[:2]
    text = line[3:]
    return (countryCode, text)

def getSentiment(text):
    thresholds = [0, 10, 25, 50, 75]
    blob = TextBlob(text)
    return (
        1,
        blob.sentiment.polarity,
        blob.sentiment.subjectivity,
        1 if (blob.sentiment.polarity >= thresholds[0]) else 0,
        1 if (blob.sentiment.polarity > thresholds[0]) else 0,
        1 if (blob.sentiment.polarity >= thresholds[1]) else 0,
        1 if (blob.sentiment.polarity > thresholds[1]) else 0,
        1 if (blob.sentiment.polarity >= thresholds[2]) else 0,
        1 if (blob.sentiment.polarity > thresholds[2]) else 0,
        1 if (blob.sentiment.polarity >= thresholds[3]) else 0,
        1 if (blob.sentiment.polarity > thresholds[3]) else 0,
        1 if (blob.sentiment.polarity >= thresholds[4]) else 0,
        1 if (blob.sentiment.polarity > thresholds[4]) else 0
    )

def rowwiseAdd(a, b):
    return tuple(map(lambda i, j: i + j, a, b))


if __name__ == "__main__":
    # create spark context with the above configuration
    sc = SparkContext(appName="TwitterStreamCovid19SentimentAnalysis")
    sc.setLogLevel("ERROR")
    # create the Streaming Context from the above spark context with interval size 100 seconds
    ssc = StreamingContext(sc, 100)

    # read data from port 9001
    tweets = ssc.socketTextStream("localhost", 9001)

    tweets\
        .map(mapToKeyValPair)\
        .mapValues(getSentiment)\
        .reduceByKey(rowwiseAdd)\
        .saveAsTextFiles(outputPath)

    # start the streaming computation
    ssc.start()
    # wait for the streaming to finish
    ssc.awaitTermination()

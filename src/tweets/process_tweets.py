from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from textblob import TextBlob
import sys
import requests

def getSentiment(line):
    blob = TextBlob(line)
    return (1, blob.sentiment.polarity, blob.sentiment.subjectivity)


def rowwiseAdd(a, b):
    return tuple(map(lambda i, j: i + j, a, b))

if __name__ == "__main__":
    # create spark context with the above configuration
    sc = SparkContext(appName="TwitterStreamCovid19SentimentAnalysis")
    sc.setLogLevel("ERROR")
    # create the Streaming Context from the above spark context with interval size 2 seconds
    ssc = StreamingContext(sc, 10)

    # read data from port 9001
    tweets = ssc.socketTextStream("localhost", 9001)

    tweets.map(getSentiment).reduce(rowwiseAdd).map(
        lambda x: (x[1] / x[0], x[2] / x[0])
    ).saveAsTextFiles('tmp')

    # start the streaming computation
    ssc.start()
    # wait for the streaming to finish
    ssc.awaitTermination()

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import sys
import requests

if __name__ == "__main__":
    # create spark context with the above configuration
    sc = SparkContext(appName="TwitterStreamCovid19SentimentAnalysis")
    sc.setLogLevel("ERROR")
    # create the Streaming Context from the above spark context with interval size 2 seconds
    ssc = StreamingContext(sc, 2)

    # read data from port 9001
    tweets = ssc.socketTextStream("localhost", 9001)

    # split each tweet into words
    words = tweets.flatMap(lambda line: line.split(" "))

    words.pprint()

    # start the streaming computation
    ssc.start()
    # wait for the streaming to finish
    ssc.awaitTermination()
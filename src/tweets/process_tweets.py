from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
import sys
import requests

# create spark configuration
conf = SparkConf()
conf.setAppName("TwitterStreamApp")
# create spark context with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
# create the Streaming Context from the above spark context with interval size 2 seconds
ssc = StreamingContext(sc, 2)
# setting a checkpoint to allow RDD recovery
ssc.checkpoint("checkpoint_TwitterApp")
# read data from port 9001
dataStream = ssc.socketTextStream("localhost",9001)

# split each tweet into words
words = dataStream.flatMap(lambda line: line.split(" "))
# filter the words to get only hashtags, then map each hashtag to be a pair of (hashtag,1)
covid = words.filter(lambda w: 'covid' in w)

covid.foreachRDD(lambda rrd: rrd.foreach(print))

# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()
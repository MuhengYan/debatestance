import json
import os
import logging
from pyspark import SparkConf, SparkContext

SPARK_APP_NAME = 'countTweet'
SPARK_MASTER = 'local[200]'
SPARK_EXECUTOR_MEMORY = '5g'

logging.basicConfig(level=logging.INFO)
_log = logging.getLogger('get_topic')


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)
    dir_path = os.path.dirname(os.path.realpath(__file__))

    _log.info("initializing Spark...")

    conf = SparkConf().setMaster(SPARK_MASTER) \
        .setAppName(SPARK_APP_NAME) \
        .set("spark.executor.memory", SPARK_EXECUTOR_MEMORY)
    sc = SparkContext(conf=conf)


    count = []
    outputFileName = ("{}/data/tweetCountByHashtags".format(dir_path))
    _log.info("Preprocessing for {}...".format(outputFileName))
    inputDirLocation = "{}/data/stance".format(dir_path)
    _log.info("Reading From {}...".format(inputDirLocation))

    # read file from s3 to rdd
    # try:
    file = sc.textFile(inputDirLocation)
    tweets = file.map(json.loads) \
        .cache()

    countHt1 = tweets \
        .filter(lambda x: x['ht1'] > 0) \
        .count()
    count.append(['Trump2016', countHt1])

    countHt2 = tweets \
        .filter(lambda x: x['ht2'] > 0) \
        .count()
    count.append(['MakeAmericaGreatAgain', countHt2])

    countHt3 = tweets \
        .filter(lambda x: x['ht3'] > 0) \
        .count()
    count.append(['ImWithHer', countHt3])

    countHt4 = tweets \
        .filter(lambda x: x['ht4'] > 0) \
        .count()
    count.append(['Hillary2016', countHt4])

    countHt5 = tweets \
        .filter(lambda x: x['ht5'] > 0) \
        .count()
    count.append(['NeverTrump', countHt5])

    countHt6 = tweets \
        .filter(lambda x: x['ht6'] > 0) \
        .count()
    count.append(['DumpTrump', countHt6])

    countHt7 = tweets \
        .filter(lambda x: x['ht7'] > 0) \
        .count()
    count.append(['DropOutHillary', countHt7])

    countHt8 = tweets \
        .filter(lambda x: x['ht8'] > 0) \
        .count()
    count.append(['NeverHillary', countHt8])

    _log.info("Saving to file ...")
    with open(outputFileName, 'w') as f:
        f.write(count)

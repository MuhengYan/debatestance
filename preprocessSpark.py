import json
import os
import logging
import filterTweets
from argparse import ArgumentParser
from pyspark import SparkConf, SparkContext
from datetime import datetime, timedelta
from settings import config

SPARK_APP_NAME = 'preprocessDebateStance'
SPARK_MASTER = 'local[200]'
SPARK_EXECUTOR_MEMORY = '5g'

logging.basicConfig(level=logging.INFO)
_log = logging.getLogger('get_topic')


if __name__ == "__main__":
    logger = logging.getLogger('Process the topic and sentiment')
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)
    dir_path = os.path.dirname(os.path.realpath(__file__))

    _log.info("initializing Spark...")

    conf = SparkConf().setMaster(SPARK_MASTER) \
        .setAppName(SPARK_APP_NAME) \
        .set("spark.executor.memory", SPARK_EXECUTOR_MEMORY)
    sc = SparkContext(conf=conf)

    c = config.Config()
    sc._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId", c.AWS_KEY)
    sc._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey", c.AWS_SECRET)

    parser = ArgumentParser(description='Extract topics from tweeters from voters tweets.')
    parser.add_argument('--all', '-a', help='extract topics from all days.', required=True)
    parser.add_argument('--day', '-d', help='number of days.', required=False)
    args = parser.parse_args()
    is_all = str(args.all)
    NUMDAYS = int(args.day)

    if is_all == "T":
        date_start = datetime(2016,11,8,16).strftime('%Y-%m-%d-%H')
        date_start = datetime.strptime(str(date_start), '%Y-%m-%d-%H')
        timeLines = [date_start - timedelta(hours=x) for x in range(0, NUMDAYS * 24)]

        date_list = ','.join([str(each_time.strftime("%m%d")) for each_time in timeLines])
        days = [str(each_time.strftime("%Y-%m-%d-%H")) for each_time in timeLines]
    else:
        now = datetime.now()
        YEAR = now.year
        MONTH = '{:02d}'.format(now.month)
        DAY = '{:02d}'.format(now.day)
        HOUR = '{:02d}'.format(now.hour - 1)
        days = ["{}-{}-{}-{}".format(YEAR, MONTH, DAY, HOUR)]

    for day in days:
        YEAR, MONTH, DAY, HOUR = day.split('-')
        outputFileName = ("{}/data/stance/{}{}{}{}_keywords".format(dir_path, YEAR, MONTH, DAY, HOUR))
        _log.info("Preprocessing for {}...".format(outputFileName))
        S3_LOCATION = "s3n://picso-lab/debate/keywords/{}/{}/{}/{}".format(YEAR, MONTH, DAY, HOUR)
        _log.info("Reading From {}...".format(S3_LOCATION))

        # read file from s3 to rdd
        # try:
        file = sc.textFile(S3_LOCATION)
        tweets = file.map(json.loads)

        tweets = tweets \
            .filter(lambda x: x['lang'] == 'en') \
            .map(filterTweets.detectTargetHashtags) \
            .filter(lambda x: x is not None) \
            .map(filterTweets.purgeTweets) \
            .map(filterTweets.getTargetStance) \
            .filter(lambda x: len(x.get("tokens")) > 0) \
            .filter(lambda x: x is not None) \
            .cache() \
            .collect()

        json_data = json.dumps(tweets,indent=4)
        final_outputFileName = '{}.json'.format(outputFileName)
        _log.info("Saving to JSON ...")
        with open(final_outputFileName, 'w') as f:
            f.write(json_data)


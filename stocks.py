import sys
import os
import datetime
import redis

from utils import (
    convert_date_to_bseurl_fmt,
    get_bse_zip_url_for_fdate,
    read_zip_file,
    read_csv_data,
)
from config import REDIS_PORT, REDIS_HOST, APP_CONFIG


class RedisStore(object):
    def __init__(self):
        if APP_CONFIG == "development":
            self.redis_ref = redis.StrictRedis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=1,
                charset="utf-8",
                decode_responses=True,
            )
        else:
            self.redis_ref = redis.from_url(
                os.environ.get("REDIS_URL"),
                db=1,
                charset="utf-8",
                decode_responses=True,
            )
        self.redis_data = None

    def store_data(self, data):
        """
        This function stores the data into Redis Server
        """
        for i, each in data.iterrows():
            self.redis_ref.rpush("ID", i)
            self.redis_ref.rpush("CODE", each["SC_CODE"])
            self.redis_ref.rpush("NAME", each["SC_NAME"].strip())
            self.redis_ref.rpush("OPEN", each["OPEN"])
            self.redis_ref.rpush("HIGH", each["HIGH"])
            self.redis_ref.rpush("LOW", each["LOW"])
            self.redis_ref.rpush("CLOSE", each["CLOSE"])
        print("All data written to Redis Database successfully")

    def get_redis(self, date=None):
        """
        This function stores the data into redis instance
        after reading and storing the csv data
        """

        date = datetime.date.today() - datetime.timedelta(days=2) if not date else date
        fdate = convert_date_to_bseurl_fmt(date)
        bse_zip_url = get_bse_zip_url_for_fdate(fdate)
        csv_file_url = read_zip_file(bse_zip_url, fdate)
        data = read_csv_data(csv_file_url)
        self.store_data(data)

    def get_top_redis_data(self):
        """
        This function returns redis stored data as dictionary having 10 records
        """
        filtered_data = {}
        for key in self.redis_ref.keys():
            filtered_data[key] = self.redis_ref.lrange(key, 0, 10)
        return filtered_data

    def search_stock_by_name(self, name):
        """
        This function returns redis stored data filtered by name of stock
        """
        ids = []
        c = 0
        p = 0
        for each in self.redis_ref.lrange("NAME", 0, -1):
            if each == name:
                ids.append(c)
            c += 1

        filtered_data = {}
        for key in self.redis_ref.keys():
            filtered_data[key] = []
            c = 0
            p = 0
            for value in self.redis_ref.lrange(key, 0, -1):
                if c == ids[p]:
                    filtered_data[key].append(value)
                    p += 1
                if p >= len(ids):
                    break
                c += 1
        return filtered_data


if __name__ == "__main__":

    if len(sys.argv) > 1:
        date = sys.argv[1]
        redis_store = RedisStore()
        redis_store.get_redis(date)
    else:
        redis_store = RedisStore()
        redis_store.get_redis()

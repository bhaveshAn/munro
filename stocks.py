import sys
import datetime
import redis

from utils import (
    convert_date_to_bseurl_fmt,
    get_bse_zip_url_for_fdate,
    read_zip_file,
    read_csv_data,
)


class RedisStore(object):
    def __init__(self):
        self.redis_ref = redis.Redis(
            host="localhost", port=6379, db=1, charset="utf-8",
            decode_responses=True
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
        This function returns the redis instance
        after reading and storing the csv data
        """

        date = datetime.datetime.today().date() if not date else date
        fdate = convert_date_to_bseurl_fmt(date)
        bse_zip_url = get_bse_zip_url_for_fdate(fdate)
        csv_file_url = read_zip_file(bse_zip_url, fdate)
        data = read_csv_data(csv_file_url)
        self.store_data(data)

    def get_redis_data(self, date=None):
        """
        This function returns redis stored data as dictionary
        """
        self.get_redis()
        self.redis_data = {}
        for key in self.redis_ref.keys():
            self.redis_data[key] = self.redis_ref.lrange(key, 0, -1)

    def get_top_redis_data(self):
        """
        This function returns redis stored data as dictionary having 10 records
        """
        self.get_redis_data()
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
        for each in self.redis_data["NAME"]:
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

    try:
        date = sys.argv[1]
        redis_store = RedisStore()
        redis_store.get_redis_data(date)
    except IndexError:
        redis_store = RedisStore()
        redis_store.get_redis_data()

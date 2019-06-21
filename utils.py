import pandas as pd
import urllib.request
import urllib
import os
from zipfile import ZipFile

from config import CSV_DIR, ZIP_DIR


def convert_date_to_bseurl_fmt(date):
    """
    This function converts date object to date format of BSE India
    http://www.bseindia.com/download/BhavCopy/Equity/EQ200619_CSV.ZIP
    """
    fdate = ""
    temp = [i for i in str(date).split("-")]
    fdate += temp[-1] + temp[1] + temp[0][-2:]
    return fdate


def get_bse_zip_url_for_fdate(fdate):
    """
    This function returns bse india url for given fdate
    http://www.bseindia.com/download/BhavCopy/Equity/EQ200619_CSV.ZIP
    """
    return "http://www.bseindia.com/download/BhavCopy/Equity/EQ" + fdate + "_CSV.ZIP"


def read_zip_file(file_url, fdate):
    """
    This function reads the zip url and stores zip file in ZIP_DIR and extracts
    the zip file in CSV_DIR
    """

    filename = os.path.join(ZIP_DIR, "EQ" + str(fdate) + ".zip")
    f = urllib.request.urlretrieve(file_url, filename)
    file = ZipFile(filename, "r")
    file.extractall(CSV_DIR)
    file.close()
    print("Zip file extracted successfully.")
    return CSV_DIR + "/EQ" + fdate + ".CSV"


def read_csv_data(csv_file_url):
    """
    This function reads he csv file and returns its data
    """
    data = pd.read_csv(
        csv_file_url,
        usecols=["SC_CODE", "SC_NAME", "OPEN", "HIGH", "LOW", "CLOSE"]
    )
    return data

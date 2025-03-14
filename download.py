"""Download L1 Data from NSMC"""

import datetime
import pytz
import requests

class Download:
    """Download L1 Data from NSMC"""

    def __init__(self, cookie: str):
        self.cookie = cookie

    def download_latest_data(self):
        """Download latest data"""
        print("START DOWNLOAD LATEST DATA...")
        data = self._list_available_data()
        if data:
            filename = data[0]["ARCHIVENAME"]
            output_path = f"./{filename}"
            self._download_data(filename, output_path)
            print("FINISH DOWNLOAD LATEST DATA!")
            return filename

    def _list_available_data(self):
        """List available data"""
        print("GETTING AVAILABLE DATA...")
        utc_now = datetime.datetime.now(pytz.utc)
        utc_now_date = utc_now.strftime("%Y-%m-%d")
        utc_now_time = utc_now.strftime("%H:%M:%S")

        utc_yesterday = utc_now - datetime.timedelta(days=1)
        utc_yesterday_date = utc_yesterday.strftime("%Y-%m-%d")
        utc_yesterday_time = utc_yesterday.strftime("%H:%M:%S")

        url = (
            "https://satellite.nsmc.org.cn/DataPortal/v1/data/selection/subfile"
            "?productID=FY4B-_AGRI--_N_DISK_1330E_L1-_FDI-_MULT_NOM_"
            "YYYYMMDDhhmmss_YYYYMMDDhhmmss_2000M_Vnnnn.HDF"
            f"&txtBeginDate={utc_yesterday_date}"
            f"&txtBeginTime={utc_yesterday_time}"
            f"&txtEndDate={utc_now_date}"
            f"&txtEndTime={utc_now_time}"
            "&east_CoordValue="
            "&south_CoordValue="
            "&west_CoordValue="
            "&north_CoordValue="
            "&cbAllArea=on"
            "&converStatus="
            "&rdbIsEvery="
            "&beginIndex=1"
            "&endIndex=100"
            "&where="
            "&timeSelection=all"
            "&periodTime="
            "&daynight="
        )
        headers = {
            "Cookie": self.cookie,
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()["resource"]

    def _download_data(self, filename: str, output_path: str):
        """Download data"""
        print("DOWNLOADING DATA...")
        url = (
            "https://satellite.nsmc.org.cn/DataPortal/v1/data/selection/file/"
            f"{filename}"
            "/download/status?downloadSource=NewPortalCH"
        )
        headers = {
            "Cookie": self.cookie,
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        real_url = response.json()["resource"]
        response = requests.get(real_url, headers=headers, timeout=10)
        response.raise_for_status()
        with open(output_path, "wb") as file:
            file.write(response.content)

"""Download L1 Data from NSMC"""

import datetime
import os
import re
import urllib

import ddddocr
import pytz
import requests


class Download:
    """Download L1 Data from NSMC"""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.session = requests.session()

    def download_latest_data(self):
        """Download latest data"""
        print("START DOWNLOAD LATEST DATA...")
        self._login(self.username, self.password)
        data = self._list_available_data()
        if data:
            filename = data[0]["ARCHIVENAME"]
            output_path = f"./{filename}"
            self._download_data(filename, output_path)
            print("FINISH DOWNLOAD LATEST DATA!")
            return filename

    def _login(self, username: str, password: str):
        """Login to NSMC"""
        print("START LOG IN NSMC")
        url = (
            "https://satellite.nsmc.org.cn/DataPortal/v1/data/user/login?"
            "newurl=https://satellite.nsmc.org.cn/DataPortal/cn/home/index.html"
        )
        response = self.session.get(url, timeout=10)
        relocate_url = response.url
        html_content = response.text
        validate_code_response = self.session.get(
            "https://fy4.nsmc.org.cn/center/v1/user/validateCode", timeout=10
        )
        with open("validateCode.jpg", "wb") as file:
            file.write(validate_code_response.content)

        ocr = ddddocr.DdddOcr()
        with open(r"./validateCode.jpg", "rb") as f:
            img_bytes = f.read()
        validate_code = ocr.classification(img_bytes)

        key_cn = urllib.parse.unquote(
            re.search(
                r'id=["\']keyCN["\'][^>]*value=["\']([^"\']+)["\']', html_content
            ).group(1)
        )

        params = relocate_url.split("?")[1].split("&")
        lk = urllib.parse.unquote(params[0].split("=")[1])
        rd = urllib.parse.unquote(params[1].split("=")[1])

        payload = {
            "loginKey": lk,
            "sourceURL": rd,
            "thePassword": self.encrypt_password(key=key_cn, passwd=password),
            "userName": username,
            "validateCode": validate_code,
        }

        commit_url = "https://fy4.nsmc.org.cn/center/v1/user/commit"
        response = self.session.post(commit_url, json=payload, timeout=10)

    def encrypt_password(self, key, passwd):
        """Get encrypted password"""
        with open("encrypt.js", "r", encoding="utf-8") as file:
            encrypt_js = file.read()
        encrypt_js = encrypt_js.replace("%KEY%", key)
        encrypt_js = encrypt_js.replace("%PASSWD%", passwd)
        with open("encrypt_modified.js", "w", encoding="utf-8") as file:
            file.write(encrypt_js)

        # exec 'node encrypt.js' and get result
        result = os.popen("node encrypt_modified.js").read()[:-1]
        return result

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

        response = self.session.get(url, timeout=10)
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
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        real_url = response.json()["resource"]
        response = self.session.get(real_url, timeout=10)
        response.raise_for_status()
        with open(output_path, "wb") as file:
            file.write(response.content)

"""Main function"""

import os
from download import Download
from render import Render
from upload import Upload


def main(
    download_cookie: str,
    upload_endpoint_url: str,
    upload_access_key: str,
    upload_secret_key: str,
):
    """Main Function"""
    dl = Download(cookie=download_cookie)
    l1_file = dl.download_latest_data()
    jpg_name = os.path.basename(l1_file).replace(".HDF", ".jpg")
    Render.render(l1_file, jpg_name)
    up = Upload(
        endpoint_url=upload_endpoint_url,
        access_key=upload_access_key,
        secret_key=upload_secret_key,
    )
    up.upload("fy-realtime", jpg_name, jpg_name)
    up.upload("fy-realtime", "latest.jpg", jpg_name)


if __name__ == "__main__":
    _download_cookie = os.getenv("DOWNLOAD_COOKIE")
    _upload_endpoint_url = os.getenv("UPLOAD_ENDPOINT_URL")
    _upload_access_key = os.getenv("UPLOAD_ACCESS_KEY")
    _upload_secret_key = os.getenv("UPLOAD_SECRET_KEY")

    main(
        download_cookie=_download_cookie,
        upload_endpoint_url=_upload_endpoint_url,
        upload_access_key=_upload_access_key,
        upload_secret_key=_upload_secret_key
    )

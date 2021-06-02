import requests
import time
import concurrent.futures

from requests.sessions import RequestsCookieJar

img_urls = [
    "https://cdn.videvo.net/videvo_files/video/free/2020-12/small_watermarked/201202_01_Oxford%20Shoppers_4k_008_preview.webm"
]

t1 = time.perf_counter()


def download_image(img_url):
    r = requests.get(img_url, stream=True)
    file_name = "Daffodil.mp4"

    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)


with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(download_image, img_urls)


t2 = time.perf_counter()

print(f'Finished in {t2-t1} seconds')

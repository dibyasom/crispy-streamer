from numpy.lib.function_base import _DIMENSION_NAME
from gcs_util import GCS
import numpy as np
import cv2 as cv
import sys
from io import BytesIO
import datetime

# Mimicing this local video file as a stream.
VIDEO_URL = "../images/cctv.mp4"
# Target bucket
BUCKET_NAME = 'calcul-datastore'

if __name__ == '__main__':
    try:
        stream = cv.VideoCapture(VIDEO_URL)
        count = 0
        while True:
            success, img = stream.read()
            if success:
                _, img_encoded = cv.imencode(".jpg", img)
                dest_file = f"{datetime.datetime.now()}.txt"

                gcs = GCS(bucket_name=BUCKET_NAME,
                          src_file=img_encoded.tobytes(),
                          dest_blob=dest_file)
                status = gcs.up()

                if not status:
                    print(f"Done-{count}")
                    count += 1

                del gcs

    # For cool exit events, no reason to exist.
    except KeyboardInterrupt as _:
        print("\nOkay, bye <3")
    '''
        < Cognitive Sorcery happenning />
    '''


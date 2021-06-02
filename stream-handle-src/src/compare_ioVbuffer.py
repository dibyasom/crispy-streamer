from gcs_util import summon_gcs
from gcs_util import GCS
import numpy as np
import cv2 as cv
import sys
from io import BytesIO
import datetime
import time
import json

import chardet

# Mimicing this local video file as a stream.
VIDEO_URL = "images/cctv.mp4"

# Target bucket
BUCKET_NAME = 'calcul-datastore'

EXC_FILE_NAME = "upload.jpg"


def numpy_to_bytes(arr: np.array) -> str:
    arr_dtype = bytearray(str(arr.dtype), 'utf-8')
    arr_shape = bytearray(','.join([str(a) for a in arr.shape]), 'utf-8')
    sep = bytearray('|', 'utf-8')
    arr_bytes = arr.ravel().tobytes()
    to_return = arr_dtype + sep + arr_shape + sep + arr_bytes
    return to_return


counter = 0
time_consumed_in_memory, time_consumed_in_io = 0, 0

if __name__ == '__main__':
    try:
        stream = cv.VideoCapture(VIDEO_URL)

        while True:
            success, img = stream.read()
            if success:
                dest_file = f"{datetime.datetime.now()}.jpg"

                t1 = time.perf_counter()  # Monitor time consumed****

                _, img_encoded = cv.imencode(".jpg", img)

                img_bytes = img_encoded.tobytes()
                print(type(img_bytes),
                      f"Encoding: {chardet.detect(img_bytes)['encoding']}")
                # gcs = GCS(bucket_name=BUCKET_NAME,
                #           src_file=img_bytes,
                #           dest_blob=dest_file)
                # status = gcs.up_file()

                t2 = time.perf_counter()  # *************************

                status = False

                if not status:
                    print(
                        "Processed via in_memory/buffer +1.")

                t3 = time.perf_counter()  # Monitor time consumed****

                cv.imwrite(EXC_FILE_NAME, img)
                _ = cv.imread(EXC_FILE_NAME)

                # gcs = GCS(bucket_name=BUCKET_NAME,
                #           src_file="upload.jpg",
                #           dest_blob=dest_file)
                # status = gcs.up_filename()

                t4 = time.perf_counter()  # *************************

                if not status:
                    print(
                        f"Processed via IO +1.")

                print(
                    f"FRAME_SIZE: {round(sys.getsizeof(img_bytes)/1024, 3)} Kb | FRAME_COUNT: {counter}\n{'*'*15}")

                time_consumed_in_memory += (t2-t1)
                time_consumed_in_io += (t4-t3)
                counter += 1

                # print(f"type(img_encoded) : {type(img_encoded)}")

                # print(
                #     f"Byte size : {round(sys.getsizeof(img_bytes)/1024, 2)}Kb\nInput image : {round(sys.getsizeof(img)/1024,2)}Kb\nNumpy bytes : {round(sys.getsizeof(img_bytes_man)/1024,2)}Kb\n{'*'*15}")

                # NOTE: DEV MODE ONLY ******************
                # gcs = GCS(bucket_name=BUCKET_NAME,
                #           src_file=img_bytes,
                #           dest_blob=dest_file)
                # status = gcs.up()
                # **************************************

                # summon_gcs.delay(img_base64, dest_file)

    # For cool exit-event-message, no reason to exist.
    except KeyboardInterrupt as _:
        print("\nOkay, bye <3")

    finally:
        # Display Analysis before exiting.
        print(f"Frames processed : {counter}")
        print(
            f"Avg proc time /frame (buffer): {round(time_consumed_in_memory/counter, 5)} second(s)")
        print(
            f"Avg proc time /frame (IO): {round(time_consumed_in_io/counter, 5)} second(s)")
#     '''
#         < Cognitive Sorcery happenning />
#     '''

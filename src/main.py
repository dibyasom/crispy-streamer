from numpy.lib.function_base import _DIMENSION_NAME
from gcs_util import summon_gcs
from gcs_util import GCS
import numpy as np
import cv2 as cv
import sys
from io import BytesIO
import datetime
import time

import os

# Mimicing this local video file as a stream.
VIDEO_URL = "../images/cctv.mp4"

# Target bucket
BUCKET_NAME = 'calcul-datastore'

# Set window size, for video chunk
WINDOW_SIZE = 3.0

# Set refresh rate
REFRESH_RATE = 3

EXC_FILE_NAME = "./upload/upload.mkv"

DIMENSION = []


def numpy_to_bytes(arr: np.array) -> str:
    arr_dtype = bytearray(str(arr.dtype), 'utf-8')
    arr_shape = bytearray(','.join([str(a) for a in arr.shape]), 'utf-8')
    sep = bytearray('|', 'utf-8')
    arr_bytes = arr.ravel().tobytes()
    to_return = arr_dtype + sep + arr_shape + sep + arr_bytes
    return to_return


counter, p_counter = 0, 0
time_consumed_in_memory = 0

if __name__ == '__main__':
    try:
        stream = cv.VideoCapture(VIDEO_URL)
        DIMENSION = (int(stream.get(3)), int(stream.get(4)), 3)
        FPS = 30

        chk_pt = time.perf_counter()  # Abs time elapsed since CPU cycle.
        start_stamp = f"{datetime.datetime.now()}"
        video_chunks_namespace = f"upload-{start_stamp}/"
        os.mkdir(video_chunks_namespace)

        first_pass = True

        CHK_PT = chk_pt

        while True:
            success, frame = stream.read()

            if success:
                if not counter:

                    t1 = time.perf_counter()  # Monitor time consumed****
                    # print(t1-chk_pt)
                    # Check if window filled?
                    if t1-chk_pt >= WINDOW_SIZE or first_pass:

                        # File name, also the start stamp.

                        if not first_pass:
                            start_stamp = f"{datetime.datetime.now()}"

                            # Release previous writer
                            writer.release()

                            # Upload file metadata.
                            upload_file_config = {
                                "from": prev_stamp,
                                "to": start_stamp,
                                "dest_file": dest_file_name
                            }

                            print(f"Adding to queue: {upload_file_config}")
                            summon_gcs.delay(upload_file_config)

                            # gcs = GCS(upload_file_config=upload_file_config)
                            # gcs.up_filename()

                        dest_file_name = f"{video_chunks_namespace}{start_stamp}.mkv"

                        writer = cv.VideoWriter(
                            dest_file_name, cv.VideoWriter_fourcc(*'MJPG'), FPS, DIMENSION[:2])

                        prev_stamp = start_stamp

                        chk_pt = t1
                        first_pass = False

                    writer.write(frame)

                    t2 = time.perf_counter()  # *************************

                    # print(
                    #     f"FRAME_SIZE: {round(sys.getsizeof(img)/1024, 3)} Kb | FRAME_COUNT: {p_counter}\n{'*'*15}")

                    time_consumed_in_memory += (t2-t1)
                    p_counter += 1

                    # NOTE: DEV MODE ONLY ******************
                    # gcs = GCS(bucket_name=BUCKET_NAME,
                    #           src_file=img_bytes,
                    #           dest_blob=dest_file)
                    # status = gcs.up()
                    # **************************************

                    if cv.waitKey(5) & 0xFF == ord('q'):
                        break

                counter = (counter + 1) % REFRESH_RATE
            else:
                break

        CHK_PT_END = time.perf_counter()

        stream.release()

    # For cool exit-event-message, no reason to exist.
    except KeyboardInterrupt as _:
        print("\nOkay, bye <3")

    except Exception as e:
        print(e)

    finally:
        # Display Analysis before exiting.
        print(f"Frames processed* : {p_counter}")
        print(
            f"Avg proc time /frame (buffer): {round(time_consumed_in_memory/p_counter, 5)} second(s)")
        print(f"Total time elapsed : {round(CHK_PT_END-CHK_PT, 3)} second(s)")

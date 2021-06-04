# :zap: crispy-streamer:tv:

### < Brief / >

<hr>

#### Source code (and explanations) for implementing the objective of uploading frames into `GCS bucket`, compute its resolution, and log the details. <br><br>I have used `docker` with custom `Dockerfile` for provisioning a fine tuned runtime for running the concurrent frame upload worker nodes, worker nodes are managed by `celery`. <br><br> Tested with sample CCTV footages (From Youtube), consistently achieved `60+ FPS` :rocket: with still a huge room for optimisation here, for instance `scene-based` resolution resizing and video compression on top of that, could significantly improve the performance beyond 100+ FPS.<br><br>

### < Working of frame uploader / >

<hr>

#### ![Uploader workflow](images/uploader-exp.png) <br>

:paperclip: `main.py`, edit this snippet in codebase, [here](https://github.com/vhaegar1526/crispy-streamer/blob/47af99e21f4b07c281a8244dfc5d2e95d224227e/gcs-celery-worker-src/src/main.py) :)

```python
# Set window size, for video chunk.
WINDOW_SIZE = 3.0

# For every X input frame, 1 frame is written to uploader.
# REFRESH_RATE represents X.
# For instance, Setting to 3, will mean, Upload every 3rd frame ...
REFRESH_RATE = 3
```

#### Uploading small video chunks, rather than individual frames because ...

- Uploading individual frames is very expensive for bandwidth, and too much dependent on network.
- For instance, uploading 50-60 FPS with individual frame upload means, 50-60 asynchronous HTTP requests every second, and a bad network would imply, all 50-60 requests to be processed v slowly, and delaying the task queue consequently.
- Uploading video in small video chunks (whose size can be tweaked with precision of miliseconds) solves the problem.
- `Maximum of 5-8 concurrent HTTP requests`, and it's more efficient, as single chunk of 3 seconds is a collection of 180 (or 90) Frames / Depending upon the FPS of source.
- `Best part -> Reduces operational overhead in cloud side, we won't have to run queing jobs to align the frames into the correct sequence, as these are time-stamp annotated video chunks, having the frames in sequence.`
- I have designed the code in a way, that it signs the metadata to every video chunk before uploading, with the exact duration of video-clip it contains, `Dataflow` can read this `Metadata` and streamline the data efficeintly for cognitive processing in later stages.

### < Microservice architecture for uploader, with celery task queue / >

<hr>

#### I have used 4 micro-services (managed by docker-compose) for isolating the all the independent services required, describing here ...

| Micro-service     | Provided Service                                                                                                     |
| ----------------- | -------------------------------------------------------------------------------------------------------------------- |
| redis             | Serves as backend for celery                                                                                         |
| rabbitmq          | Serves as message borker for celery                                                                                  |
| gcs-celery-worker | Provisions worker nodes for concurrent uploads                                                                       |
| stream-handle     | Accepts RTSP/Video stream, implements windowing for breaking into chunks, calls celery-app asynchronously once done. |

#### Explanation and file structure, how I made sure `gcs-celery-worker` and `stream-handle` work on the same filespace (As required by celery to be callable).

![Docker fs](images/docker-fs.png)

##### I have implemented docker-named-mounts, where in the containers can write video chunks, and can be efficently shared by worker-nodes to be used, without needing to transfer the file bw containers.<br><br>

### < Cloud Architecture to process the frames, once received / >

<hr>

![Cloud implemented architecture](images/cloud-arch.png)

- Video chunks are written to `GCS bucket`
- `GCS events` configured for `publishing` the `FINALIZE-OBJECT` event upon received video chunk.
- `pub-sub` triggers the `google-cloud-function` as a subscriber, and processes the data by streaming the video file, and logs the
  1. `Video Resolution` (Length, breadth and color-channels)
  2. `Duration` (Exact duration for which the video chunk has the clip, read from `METADATA` as signed by the local-uploader, during creation.)
  3. `mediaLink` for accessing the video-chunk, this is crucial, as all further processes within Google-Cloud can use this URL securely to run `inferences` and is already annotated with the exact `time-stamp`.

#### Some snapshots of the generated logs ...

![Log groped](images/log-group.png)

#### Zooming in ... :mag:

![Log zommed in <3](images/log-zoomed-in.png)

<hr>

### Limitations

- Atleast 8 gigs of RAM is required for running all the micro-services in parallel , under my testings it peaked out at little more than 7GB, and will linearly increase to stream from different sources simultaneously.

### Risks

- Service account credentials (as JSON) is present within docker image, in production I would be passing it as environment vairable, but for quicker dev and testing, I have made it available within docker itself _[FIXED NOW, using docker-bind-mount and exposing via environment variable]_.
- Uploader works with the semantic of `try once` I have not configured it for retrying upload in case the current upload fails, with some tweaks it can be set to retry upon failure, it's doable.

### Scalabilty

- SCALABILTY is unbounded, I have built the source code, with one goal of making it serverless as much as possible, on premise, the docker-compose setup does not depend on and HOST or IO transaction for communicating or sharing files, rather I have used docker managed volumes, which makes it capable to spin-up and down or scale horizontally as and when required.

<hr>

### Coming to what could be done better?

- Integration of `Cloud Dataflow` could automate the process of ingesting data-streaming, monitoring and modelling, but as it has a peeky learning curve, I couldn't integrate it under the given time constraints, but I would be happy to learn and integrate it in future.

- `stream-handle` writes the video as raw byte strings, with .mkv container, which makes the file to be uploaded of size larger than it should be, I plan to use video compressions, to reduce this significantly, and it can boost the upload processing speeds (currently ~ 60+ FPS) to more than 100 FPS, for sure.

- `docker-compose` is what I have used here, to provision and isolate seprate containers for the different micro-services to run in, as good as it is, using Kubernetes would have been better, as it has
  - Healing attributes for container
  - Retries automatically if container fails or provisions a new one instantly, and
  - Can be managed and monitored by cloud dashboards.

<hr>

### Testing the system.

To test the system, there a few pre-requisites to be satisfied,

- Docker and docker-compose installed in the system. (podman and podman-compose will work fine too, tested already.)
- Google service account credentials, with sufficient permissions to write, and create buckets (If not already created). [In production, I would make sure credentials are passed as environment variable, rather than manual upload]

#### _Steps for testing_

> Rename the service account credential as `creds.json` and place it in, `gcs-celery-worker-src`/

> Rename the video file to be uploaded as `cctv.mp4` and do place it in, `stream-handle-src`/`src`/

> Just open the root directory of the project, and run `sudo docker-compose up`

_NOTE_ : In practice it will be a RTSP stream, that can be accessed in real-time, or I would setup a docker bind-mount to provide the video file in real-time, for now I have hardcoded it to `cctv.mp4`.

<hr>

Apart from all the limitations and risks I have stated, there might be some more, that I'm not aware of, do let me know about those, I'll be happy to rectify those.

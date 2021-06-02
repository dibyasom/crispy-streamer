# :zap: crsipy-streamer :rocket:

### < Brief / >

<hr>

#### Source code (and explanations) for implementing the objective of uploading frames into `GCS bucket`, compute its resolution, and log the details. <br><br>I have used `docker` with custom `Dockerfile` for provisioning a fine tuned runtime for running the concurrent frame upload worker nodes, worker nodes are managed by `celery`. <br><br> Tested with sample CCTV footages (From Youtube), consistently achieved `60+ FPS :rocket:` with still a huge room for optimisation here, I'm sure it can achieve 120 FPS, like compressing the video, right now I'm uploading raw binaries (Due to time cnstraint haven't worked on compression yet).<br><br>

### < Working of frame uploader / >

<hr>

#### ![Uploader workflow](images/uploader-exp.png) <br> Uploading small video chunks, rather than individual frames because ...
- Uploading individual frames is very expensive for bandwidth, and too muc dependent on network.
- For instance, uploading 50~60 FPS with individual frame upload means, 50~60 asynchronous HTTP requests every second, and a bad network would imply, all 50~60 requests to be processed v slowly, and delying the task queue consequently.
- `Uploading video in small video chunks (whose size can be twekes with precision of miliseconds) solves the problem.`
- `Maximum of 5-8 concurrent HTTP request, and it's more efficient, as single chunk of 3 secs is a collection of 180 (or 90) Frames`
- `Best part -> Reduces operational overhead in cloud side, we won't have to run queing jobs to align the frames into the correct sequence, as these are video chunks, having the frames in sequence.`
- I have designed the code in a way, that it signs the metadata to every video chunk before uploading, with the exact duration of video-clip it contains, `Dataflow` can read this `Metadata` and streamline the data efficeintly for cognitive  

#### Modelling the data (Frames from RTSP/Video) for uploading could be done by, 
- Writing inidividual frames to disk
- Mantaining an array/object for processed and uploaded frames
- Uploading the file by frame.

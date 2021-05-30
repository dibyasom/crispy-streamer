from google.cloud import storage


class GCS:

    def __init__(self, bucket_name, src_file, dest_blob) -> None:
        self.bucket_name = bucket_name
        self.source_file_name = src_file
        self.destination_blob_name = dest_blob

    def up(self) -> int:
        """Uploads a file to the bucket."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"
        # The path to your file to upload
        # source_file_name = "local/path/to/file"
        # The ID of your GCS object
        # destination_blob_name = "storage-object-name"

        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)

        blob = bucket.blob(self.destination_blob_name)

        try:
            blob.upload_from_string(self.source_file_name,
                                    content_type="text/plain")
            return 0
        # print(blob._get_writable_metadata)
        except Exception as e:
            print(e)
            return 1

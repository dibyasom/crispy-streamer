from google.cloud import storage
from celery_app import app

# Target bucket
BUCKET_NAME = 'calcul-datastore'


@app.task
def summon_gcs(upload_file_config):

    gcs = GCS(
        upload_file_config=upload_file_config)
    gcs.up_filename()

    # Dispose once done
    del gcs


class GCS:

    def __init__(self, upload_file_config) -> None:
        self.bucket_name = BUCKET_NAME
        self.upload_file_config = upload_file_config

    def up_file(self) -> int:
        """Uploads a file to the bucket."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"
        # The path to your file to upload
        # source_file_name = "local/path/to/file"
        # The ID of your GCS object
        # destination_blob_name = "storage-object-name"

        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)

        # TODO: Optimise for batch uploads.
        blob = bucket.blob(self.destination_blob_name)

        try:
            url = blob.upload_from_string(self.source_file_name,
                                          content_type="image/jpg")
            return url
        # print(blob._get_writable_metadata)
        except Exception as e:
            print(e)
            return 1

    def up_filename(self) -> int:
        """Uploads a file to the bucket."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"
        # The path to your file to upload
        # source_file_name = "local/path/to/file"
        # The ID of your GCS object
        # destination_blob_name = "storage-object-name"

        storage_client = storage.Client.from_service_account_json(
            '/build/assets/creds.json')
        bucket = storage_client.bucket(self.bucket_name)

        # TODO: Optimise for batch uploads.
        file_name = self.upload_file_config.pop('dest_file', '-1')
        blob = bucket.blob(file_name)

        blob.metadata = self.upload_file_config

        try:
            url = blob.upload_from_filename(file_name)
            return url
        # print(blob._get_writable_metadata)
        except Exception as e:
            return e

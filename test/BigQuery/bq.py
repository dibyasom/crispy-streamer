from google.cloud import bigquery
import six

bq_client = bigquery.Client()
table_id = "incubate-fellows.stream_log.log"

job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("from", "STRING"),
        bigquery.SchemaField("to", "STRING"),
        bigquery.SchemaField("mediaLink", "STRING"),
        bigquery.SchemaField("resolution", "STRING"),
    ],
)

body = six.BytesIO(b"Washington,WA")
bq_client.load_table_from_file(body, table_id, job_config=job_config).result()
previous_rows = bq_client.get_table(table_id).num_rows
assert previous_rows > 0

job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
)

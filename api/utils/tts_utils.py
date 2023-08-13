from google.cloud import storage

def upload_blob_from_memory(bucket_name, contents, destination_blob_name):
    """Uploads a file to the bucket."""

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The contents to upload to the file
    # contents = "these are my contents"

    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(contents)
    blob.make_public()
    public_url = blob.public_url

    print(
        f"{destination_blob_name} with contents {contents} uploaded to {bucket_name} with public url {public_url}."
    )

    return public_url


def concatenate_characters(array):
    return ''.join(''.join(subarray) for subarray in array)
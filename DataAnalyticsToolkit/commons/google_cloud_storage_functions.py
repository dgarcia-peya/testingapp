from google.cloud import storage


def upload_file(bucket_name, destination_name, file_path):
    """

    :param bucket_name: The destination Google Storage Bucket
    :param destination_name: The destination file path in Google Storage Bucket
    :param file_path: Path to the local file to be uploaded
    :return: Dict. Error is True if an exception occurs during the upload
    """
    try:

        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_name)

        blob.upload_from_filename(file_path)

        return {"error": False}

    except Exception as e:
        return {"error": True, "message": e.message}

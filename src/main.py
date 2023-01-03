import boto3
import uuid
import time


s3_resource = boto3.resource("s3")
s3_client = boto3.client("s3")


def create_temp_file(size, file_name, file_content, slice_len=6):
    # by adding randomness to our file name, we can efficiently distribute
    # our data within our s3 bucket
    random_file_name = "".join([str(uuid.uuid4().hex[:slice_len]), file_name])
    with open(random_file_name, "w") as f:
        f.write(str(file_content) * size)
    return random_file_name


def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    # uuid gives 36 char long string representation(including hyphens)
    return "".join([bucket_prefix, str(uuid.uuid4())])


def create_bucket(bucket_prefix, s3_connection):
    """Create a bucket with the given prefix name

    Args:
        bucket_prefix (str): name that specifies what the bucket is for
        s3_connection (_type_): client or resource methods from boto3

    Returns:
        tuple: bucket name and the bucket response object
    """
    session = boto3.session.Session()
    current_region = session.region_name
    bucket_name = create_bucket_name(bucket_prefix=bucket_prefix)
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={"LocationConstraint": current_region},
    )
    print(bucket_name, current_region)
    return bucket_name, bucket_response


def copy_to_bucket(bucket_from_name, bucket_to_name, file_name):
    copy_source = {"Bucket": bucket_from_name, "Key": file_name}
    s3_resource.Object(bucket_to_name, file_name).copy(copy_source)


if __name__ == "__main__":
    # the response here is a dictionary with much more information
    first_bucket_name, first_bucket_response = create_bucket(
        bucket_prefix="firstpythonbucket", s3_connection=s3_resource.meta.client
    )

    # the response here is a resources.factory.s3.Bucket obj
    # contains the bucket name and fewer info than the client
    second_bucket_name, second_bucket_response = create_bucket(
        bucket_prefix="secondpythonbucket", s3_connection=s3_resource
    )

    first_file_name = create_temp_file(300, "firstfile.txt", "f")

    first_bucket = s3_resource.Bucket(name=first_bucket_name)
    first_object = s3_resource.Object(
        bucket_name=first_bucket_name, key=first_file_name
    )

    # provide the path to the file
    first_object.upload_file(first_file_name)

    # Downloading a file
    s3_resource.Object(first_bucket_name, first_file_name).download_file(
        f"/tmp/{first_file_name}"
    )

    # Copy files from 1st bucket to the 2nd bucket
    copy_to_bucket(
        bucket_from_name=first_bucket_name,
        bucket_to_name=second_bucket_name,
        file_name=first_file_name,
    )
    
    time.sleep(30)
    # Deleting a file from a bucket
    print("Deleting the file")
    s3_resource.Object(second_bucket_name, first_file_name).delete()

import boto3
import uuid


s3_resource = boto3.resource("s3")
s3_client = boto3.client("s3")


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


# the response here is a dictionary with much more information
first_bucket_name, first_bucket_response = create_bucket(
    bucket_prefix="firstpythonbucket", s3_connection=s3_resource.meta.client
)


# the response here is a resources.factory.s3.Bucket obj
# contains the bucket name and fewer info than the client
second_bucket_name, second_bucket_response = create_bucket(
    bucket_prefix="secondpythonbucket", s3_connection=s3_resource
)

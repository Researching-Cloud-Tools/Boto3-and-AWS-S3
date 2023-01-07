from main import *

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

    second_file_name = create_temp_file(400, 'secondfile.txt', 's')
    second_object = s3_resource.Object(first_bucket.name, second_file_name)
    second_object.upload_file(second_file_name, ExtraArgs={
                            'ACL': 'public-read'})
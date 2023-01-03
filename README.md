# Boto3-and-AWS-S3

- [Before getting started](#before-getting-started)
- [What is Boto3?](#boto3)
- [Operations on S3](#common-operations)

  - [Bucket Creation](#creating-a-bucket)
    - [Bucket and Object Instance Creation](#creating-a-bucket-and-object-instance)
  - [Uploading a File](#uploading-a-file-to-s3)

    - [From an Object Instance](#1-from-an-object-instance)
    - [From a Bucket Instance](#2-from-a-bucket-instance)
    - [From the client](#3-from-the-client)

  - [Downloading a File](#downloading-a-file)
  - [Copying an Object Between Buckets](#copying-an-object-between-buckets)
  - [Deleting an Object](#deleting-an-object)

## Before getting started

- Use a IAM user with **AmazonS3FullAccess** policy. This allows the user to have full control over S3
- make sure the `~/.aws/config` and `~/.aws/credentials` are properly configured with the above use
- if in doubt follow [this tutorial](https://realpython.com/python-boto3-aws-s3/)
- [Naming Convention for better use of S3](https://aws.amazon.com/blogs/aws/amazon-s3-performance-tips-tricks-seattle-hiring-event/)

## Boto3

- Boto3 calls the AWS APIs on our behalf and that's how it works at its core.
- For the majority of the AWS services, Boto3 offers 2 distinct ways of accessing these abstracted APIs

### i) **Client**: low-level service access

        - `boto3.client("s3")`
        - majority gives a dictionary response from which we'll need to parse it ourselves i.e this one requires more programmatic approach
        - there might be a slight performance improvements with a loss in readability
        - generated from JSON service definition file
        - the client methods support every single type of interaction with the target AWS service

### ii) **Resource**: higher-level object-oriented service access

        - `s3_resource = boto3.resource("s3")`
        - The SDK does the parsing stuff for us
        - might be slighly slower but offers better abstraction and readability
        - generated from JSON resource definition file
        - we can access the client directly via the resource using `s3_resource.meta.client` so we don't need to change our code to use the client everywhere
            - once such client operation is `.generate_presigned_url()`
            - this enables us to give our users access to an object within our bucket for a set period of time, without requiring them to have AWS credentials.

> We can use either of these to interact with S3

## Common Operations

### Creating a Bucket

- Bucket name are DNS complaint so they must be unique throughout the WHOLE AWS PLATFORM. There's a error for that `botocore.errorfactory.BucketAlreadyExists`
- If our region is not in the United States then we need to explicitly define our region while creating a bucket. or face the `IllegalLocationConstraintException` error

  ```py
  s3_resource.create_bucket(Bucket=BUCKET_NAME, CreateBucketConfiguration={
  "LocationConstraint": 'ap-south-1'
  })
  ```

- we can also get the region programatically, by taking advantage of a session object.
  - Boto3 will create the session from our credentials.
  - We can then get the region from `boto3.session.Session().region_name()`

#### Creating a Bucket and Object instance

- Bucket and Object are sub-resources of one another.
  - Sub-resources are methods that create a new instance of a child resource.
  - the parent's identifiers get passed to the child resource
- we can use the abstraction that resource provides to create a bucket
  `first_bucket = s3_resource.Bucket(name=first_bucket_name)`
- for the Object, Boto3 doesn't make calls to AWS to create the reference.

  ```py
  first_object = s3_resource.Object(
  bucket_name=first_bucket_name, key=first_file_name)
  ```

  - this doesn't make changes to the s3 on aws
  - `bucket_name` and the `key` are called identifiers, and they are the necessary parameters to create an Object
  - other parameters of an Object like its size are lazily loaded.
  - this means that for Boto3 to get the requested attributes, it has to make calls to AWS

- we can also create an Object directly if we have a Bucket variable
  `first_obj_again = first_bucket.Object(first_file_name)`
- Or, if we have an Object variable, then we can get the Bucket
  `first_bucket_again = first_object.Bucket()`

### Uploading a File to S3

- There are 3 ways to upload a file.
- In all these cases we must provide the path of the file we want to upload

#### 1) From an Object Instance

```py
s3_resource.Object(first_bucket_name, first_file_name).upload_file(
    Filename=first_file_name)
```

OR,

`first_object.upload_file(first_file_name)`

#### 2) From a Bucket Instance

- as the bucket_name and key are necessary to create the Object we pass those.

```py
s3_resource.Bucket(first_bucket_name).upload_file(
    Filename=first_file_name, Key=first_file_name)
```

#### 3) From the client

```py
s3_resource.meta.client.upload_file(
    Filename=first_file_name, Bucket=first_bucket_name,
    Key=first_file_name)
```

### Downloading A File

- the steps are similar to uploading.
- Filename now will map to our desired local path

```py
  s3_resource.Object(first_bucket_name, first_file_name).download_file(
  f'/tmp/{first_file_name}')
```

### Copying an Object Between Buckets

- if we need to copy files from one bucket to another, Boto3 offers us that possibility with `.copy()`

```py
def copy_to_bucket(bucket_from_name, bucket_to_name, file_name):
    copy_source = {
        'Bucket': bucket_from_name,
        'Key': file_name
    }
    s3_resource.Object(bucket_to_name, file_name).copy(copy_source)
```

> For Copying or replicating our S3 objects to a bucket in a different region, use [Cross Region Replication](https://docs.aws.amazon.com/AmazonS3/latest/dev/crr.html)

### Deleting an Object

- we can delete the file from bucket by calling `.delete()` on the equivalent Object instance.
`s3_resource.Object(second_bucket_name, first_file_name).delete()`

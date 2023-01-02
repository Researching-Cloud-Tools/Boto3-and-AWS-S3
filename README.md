# Boto3-and-AWS-S3

## Before getting started

- Use a IAM user with **AmazonS3FullAccess** policy. This allows the user to have full control over S3
- make sure the `~/.aws/config` and `~/.aws/credentials` are properly configured with the above use
- if in doubt follow [this tutorial](https://realpython.com/python-boto3-aws-s3/)

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

  ```
  s3_resource.create_bucket(Bucket=BUCKET_NAME, CreateBucketConfiguration={
  "LocationConstraint": 'ap-south-1'
  })
  ```

- we can also get the region programatically, by taking advantage of a session object.
  - Boto3 will create the session from our credentials.
  - We can then get the region from `boto3.session.Session().region_name()`
  

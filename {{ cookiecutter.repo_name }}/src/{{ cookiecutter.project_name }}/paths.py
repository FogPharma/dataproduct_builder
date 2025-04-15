from cloudpathlib import S3Path

# Create a path S3 object
# Call `project_s3 / 'new_directory'` in your code in a `pathlib.Path` way.
# Read more about `cloudpathlib.S3Path` here: https://cloudpathlib.drivendata.org/stable/api-reference/s3path/
project_s3 = S3Path("s3://bucket/key")

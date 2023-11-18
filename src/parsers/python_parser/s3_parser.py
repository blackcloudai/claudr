import boto3
from botocore.exceptions import ClientError

def parse_s3_ls_command(command):
    """
    Parses the 'aws s3 ls' command and returns equivalent Python code.

    Parameters:
    command (str): The AWS CLI command to parse.

    Returns:
    str: Python code equivalent of the command.
    """
    # Split the command to analyze its parts
    parts = command.split()

    # Check if the command is to list buckets or contents of a specific bucket
    if len(parts) == 3 and parts[2].startswith("s3://"):
        bucket_name = parts[2][5:]  # Extract bucket name
        return list_bucket_contents_code(bucket_name)
    elif len(parts) == 2:
        return list_all_buckets_code()
    else:
        return "Invalid 'aws s3 ls' command."

def list_all_buckets_code():
    """
    Generates Python code to list all S3 buckets.

    Returns:
    str: Python code for listing all buckets.
    """
    code = f"""
                import boto3

                s3 = boto3.client('s3')
                response = s3.list_buckets()
                for bucket in response['Buckets']:
                    print(bucket['Name'])
            """
    return code

def list_bucket_contents_code(bucket_name):
    """
    Generates Python code to list contents of a specific S3 bucket.

    Parameters:
    bucket_name (str): The name of the bucket.

    Returns:
    str: Python code for listing contents of the specified bucket.
    """
    code = f"""
                import boto3

                s3 = boto3.client('s3')
                response = s3.list_objects_v2(Bucket='{bucket_name}')
                if 'Contents' in response:
                    for item in response['Contents']:
                        print(item['Key'])
                else:
                    print("No items in bucket.")
            """
    return code

def parse_s3_mb_command(command):
    """
    Parses the 'aws s3 mb' command and returns equivalent Python code.

    Parameters:
    command (str): The AWS CLI command to parse.

    Returns:
    str: Python code equivalent of the command.
    """
    parts = command.split()

    # Check if the command is to create a new bucket
    if len(parts) >= 3 and parts[2].startswith("s3://"):
        bucket_name = parts[2][5:]  # Extract bucket name
        # Optional: Handle region or other flags if present in the command
        return create_bucket_code(bucket_name)
    else:
        return "Invalid 'aws s3 mb' command."

def create_bucket_code(bucket_name):
    """
    Generates Python code to create an S3 bucket.

    Parameters:
    bucket_name (str): The name of the bucket to create.

    Returns:
    str: Python code for creating the specified bucket.
    """
    code = f"""
                import boto3
                from botocore.exceptions import ClientError

                def create_bucket(bucket_name, region=None):
                    s3 = boto3.client('s3')
                    try:
                        if region is None:
                            s3.create_bucket(Bucket=bucket_name)
                        else:
                            location = {{'LocationConstraint': region}}
                            s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
                    except ClientError as e:
                        print(f"ERROR: {{e}}")
                        return False
                    return True

                # Create the bucket
                create_bucket('{bucket_name}')
            """
    return code

def parse_s3_cp_command(command):
    """
    Parses the 'aws s3 cp' command and returns equivalent Python code.

    Parameters:
    command (str): The AWS CLI command to parse.

    Returns:
    str: Python code equivalent of the command.
    """
    parts = command.split()
    
    # Example command format: aws s3 cp local_file s3://bucket_name/destination_file
    if len(parts) == 4 and parts[3].startswith('s3://'):
        source_file = parts[2]
        bucket_info = parts[3][5:].split('/')
        bucket_name = bucket_info[0]
        destination_file_name = '/'.join(bucket_info[1:])
        return copy_file_to_bucket_code(bucket_name, source_file, destination_file_name)
    else:
        return "Invalid 'aws s3 cp' command."

def copy_file_to_bucket_code(bucket_name, source_file, destination_file_name):
    """
    Generates Python code to copy a file to an S3 bucket.

    Parameters:
    bucket_name (str): The name of the bucket.
    source_file (str): The local file to upload.
    destination_file_name (str): The destination file name in the bucket.

    Returns:
    str: Python code for copying a file to an S3 bucket.
    """
    code = f"""
                import boto3
                from botocore.exceptions import ClientError

                s3 = boto3.client('s3')
                try:
                    with open('{source_file}', 'rb') as data:
                        s3.upload_fileobj(data, '{bucket_name}', '{destination_file_name}')
                    print("File uploaded successfully.")
                except ClientError as e:
                    print(f"ERROR: {{e}}")
            """
    return code

def parse_s3_rb_command(command):
    """
    Parses the 'aws s3 rb' command and returns equivalent Python code.

    Parameters:
    command (str): The AWS CLI command to parse.

    Returns:
    str: Python code equivalent of the command.
    """
    parts = command.split()
    
    # Example command format: aws s3 rb s3://bucket-name
    if len(parts) == 3 and parts[2].startswith('s3://'):
        bucket_name = parts[2][5:]  # Extract bucket name
        return delete_bucket_code(bucket_name)
    else:
        return "Invalid 'aws s3 rb' command."

def delete_bucket_code(bucket_name):
    """
    Generates Python code to delete an S3 bucket.

    Parameters:
    bucket_name (str): The name of the bucket to delete.

    Returns:
    str: Python code for deleting an S3 bucket.
    """
    code = f"""
                import boto3
                from botocore.exceptions import ClientError

                s3 = boto3.client('s3')
                try:
                    s3.delete_bucket(Bucket='{bucket_name}')
                    print("Bucket '{bucket_name}' deleted successfully.")
                except ClientError as e:
                    print(f"ERROR: {{e}}")
            """
    return code

def download_file_from_s3(bucket_name, s3_object_key, local_file_path):
    """
    Download a file from an S3 bucket.

    Parameters:
    bucket_name (str): The name of the S3 bucket.
    s3_object_key (str): The key (path) of the object in the bucket.
    local_file_path (str): The local path where the file will be downloaded.

    Returns:
    bool: True if download was successful, False otherwise.
    """
    s3_client = boto3.client('s3')
    try:
        s3_client.download_file(bucket_name, s3_object_key, local_file_path)
        print(f"File '{s3_object_key}' downloaded successfully to '{local_file_path}'.")
        return True
    except ClientError as e:
        print(f"Error downloading file: {e}")
        return False

# Example usage:
download_file_from_s3('my-bucket', 'path/to/s3/object.txt', 'path/to/local/file.txt')
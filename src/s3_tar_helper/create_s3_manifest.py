import argparse
import csv

import boto3


def create_s3_manifest(bucket_name, output_file="s3_manifest.csv"):
    """
    Creates a CSV manifest of objects in an S3 bucket including bucket, key, and content-length.

    Args:
        bucket_name (str): The name of the S3 bucket.
        output_file (str): The name of the output CSV file.
    """
    s3 = boto3.client("s3")
    manifest_data = []

    print(f"Generating manifest for bucket: {bucket_name}...")

    try:
        paginator = s3.get_paginator("list_objects_v2")
        # Use a custom page size if desired, e.g., PaginationConfig={'PageSize': 1000}
        pages = paginator.paginate(Bucket=bucket_name)

        found_objects = False
        for page in pages:
            if "Contents" in page:
                found_objects = True
                for obj in page["Contents"]:
                    key = obj["Key"]
                    size = obj["Size"]  # Size is content-length in bytes
                    manifest_data.append(
                        {"Bucket": bucket_name, "Key": key, "Content-Length": size}
                    )

        if manifest_data:
            with open(output_file, "w", newline="") as csvfile:
                fieldnames = ["Bucket", "Key", "Content-Length"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for row in manifest_data:
                    writer.writerow(row)
            print(f"Manifest created successfully: {output_file}")
        elif not found_objects:  # If no objects were found across all pages
            print(
                f"No objects found in bucket: {bucket_name}. No manifest file was created."
            )
        else:  # Should not happen if manifest_data is empty but found_objects is true
            print(
                "No manifest generated, but objects were listed (this is unexpected)."
            )

    except s3.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchBucket":
            print(f"Error: Bucket '{bucket_name}' does not exist.")
        elif e.response["Error"]["Code"] == "AccessDenied":
            print(
                f"Error: Access denied to bucket '{bucket_name}'. Check your AWS credentials and permissions."
            )
        else:
            print(f"An AWS S3 error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def parse_args():
    parser = argparse.ArgumentParser(description="Create S3 manifest from bucket")
    parser.add_argument("bucket_name", help="S3 bucket name to create manifest for")
    parser.add_argument(
        "--output-file",
        default="s3_manifest.csv",
        help="Output CSV file name (default: s3_manifest.csv)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    bucket_arg = args.bucket_name
    output_file_arg = args.output_file
    create_s3_manifest(bucket_arg, output_file_arg)

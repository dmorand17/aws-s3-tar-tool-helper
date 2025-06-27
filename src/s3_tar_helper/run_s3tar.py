# run_s3tar_for_manifests.py
# Run on s3tar manifests
import argparse
import os
import subprocess


def parse_args():
    parser = argparse.ArgumentParser(description="Run s3tar on manifests")
    parser.add_argument(
        "--manifest-dir",
        default="/home/ec2-user/data/manifests",
        help="Directory containing manifest files (default: /home/ec2-user/data/manifests)",
    )
    parser.add_argument(
        "--dest-bucket", required=True, help="Destination S3 bucket name"
    )
    parser.add_argument(
        "--s3tar-path",
        default="./s3tar",
        help="Path to s3tar executable (default: ./s3tar)",
    )
    parser.add_argument(
        "--region",
        default=os.environ.get("AWS_REGION", "us-east-2"),
        help="AWS region (default: from AWS_REGION env var, fallback to us-east-2)",
    )

    return parser.parse_args()


def run_s3tar(args):
    MANIFEST_DIR = args.manifest_dir
    DEST_BUCKET = args.dest_bucket
    S3TAR_PATH = args.s3tar_path
    REGION = args.region

    for filename in os.listdir(MANIFEST_DIR):
        if not filename.endswith(".csv"):
            continue

        manifest_path = os.path.join(MANIFEST_DIR, filename)
        name = filename[:-4]  # strip '.csv'
        output_path = f"s3://{DEST_BUCKET}/tars/{name}.tar"

        cmd = [S3TAR_PATH, "--region", REGION, "-cvf", output_path, "-m", manifest_path]

        print(f"Running: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
            print(f"✅ Success: {name}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed: {name}")


if __name__ == "__main__":
    args = parse_args()
    run_s3tar(args)

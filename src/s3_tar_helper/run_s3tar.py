# run_s3tar_for_manifests.py
# Run on s3tar manifests
import argparse
import os
import subprocess


def parse_args():
    parser = argparse.ArgumentParser(description="Run s3tar on manifests")
    parser.add_argument(
        "--manifest-dir",
        default="manifests",
        help="Directory containing manifest files (default: manifests)",
    )
    parser.add_argument(
        "--dest-bucket", required=True, help="Destination S3 bucket name"
    )
    parser.add_argument(
        "--region",
        default=os.environ.get("AWS_REGION", "us-east-2"),
        help="AWS region (default: from AWS_REGION env var, fallback to us-east-2)",
    )
    parser.add_argument(
        "--concat-in-memory",
        action="store_true",
        help="Use the --concat-in-memory option with s3tar (in-memory tarball generation)",
    )

    return parser.parse_args()


def run_s3tar(args):
    MANIFEST_DIR = args.manifest_dir
    DEST_BUCKET = args.dest_bucket
    REGION = args.region

    for filename in os.listdir(MANIFEST_DIR):
        if not filename.endswith(".csv"):
            continue

        manifest_path = os.path.join(MANIFEST_DIR, filename)
        name = filename[:-4]  # strip '.csv'
        output_path = f"s3://{DEST_BUCKET}/tars/{name}.tar"

        cmd = ["s3tar", "--region", REGION, "-cvf", output_path, "-m", manifest_path]
        if args.concat_in_memory:
            cmd.append("--concat-in-memory")

        print(f"Running: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
            print(f"✅ Success: {name}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed: {name}")


def main():
    args = parse_args()
    run_s3tar(args)


if __name__ == "__main__":
    main()

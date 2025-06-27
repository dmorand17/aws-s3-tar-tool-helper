# AWS S3 Tar Helper

A Python helper project for working with the [amazon-s3-tar-tool](https://github.com/awslabs/amazon-s3-tar-tool) to create S3 bucket manifests and automate s3tar operations. This project provides complementary tools to generate CSV manifests of S3 bucket contents and execute s3tar commands for bulk operations.

## Overview

The [amazon-s3-tar-tool](https://github.com/awslabs/amazon-s3-tar-tool) is a powerful Go-based utility that creates tarballs of existing objects in Amazon S3 using multipart uploads. This helper project extends its functionality by providing:

- **Automated manifest generation**: Create CSV manifests of S3 bucket contents for use with s3tar
- **Batch processing**: Run s3tar operations across multiple manifest files
- **Python-based workflow**: Easy integration with Python-based data processing pipelines

## How It Works

1. **Generate Manifests**: Use this helper to create CSV manifests of your S3 bucket contents
2. **Process with s3tar**: Feed the manifests to the amazon-s3-tar-tool to create tarballs
3. **Automate Workflows**: Batch process multiple buckets or directories

## Features

- **S3 Manifest Creation**: Generate CSV manifests of S3 bucket contents with bucket, key, and content-length information
- **S3Tar Integration**: Run s3tar commands on manifest files for bulk S3 operations
- **UV Integration**: Modern Python dependency management with UV
- **Command Line Tools**: Installable scripts for easy command-line access
- **Batch Processing**: Process multiple manifest files automatically

## Prerequisites

- Python 3.13+ (as specified in `.python-version`)
- [UV](https://docs.astral.sh/uv/) - Fast Python package installer and resolver
- AWS credentials configured (via AWS CLI, environment variables, or IAM roles)
- [amazon-s3-tar-tool](https://github.com/awslabs/amazon-s3-tar-tool) - The main s3tar executable

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd aws-s3-tar-tool-helper
   ```

2. **Install dependencies with UV**:

   ```bash
   uv sync
   ```

   This will:

   - Create a virtual environment
   - Install all dependencies from `pyproject.toml`
   - Use the Python version specified in `.python-version`

3. **Install amazon-s3-tar-tool**:

   ```bash
   # Download the latest release
   curl -L https://github.com/awslabs/amazon-s3-tar-tool/releases/latest/download/s3tar -o s3tar
   chmod +x s3tar
   sudo mv s3tar /usr/local/bin/
   ```

## Usage

This project provides two main tools that can be run using `uv run`. The `uv run` command automatically handles the virtual environment and dependencies, making it the recommended way to execute the scripts.

### 1. Creating S3 Manifests

Generate a CSV manifest of objects in an S3 bucket using the `create-s3-manifest.py` script. This creates the input files needed for the amazon-s3-tar-tool:

```bash
# Basic usage - creates s3_manifest.csv in current directory
uv run python src/s3_tar_helper/create-s3-manifest.py my-bucket-name

# Specify custom output file
uv run python src/s3_tar_helper/create-s3-manifest.py my-bucket-name --output-file my-manifest.csv

# Using the installed command-line tool (alternative)
uv run create-manifests my-bucket-name
uv run create-manifests my-bucket-name --output-file my-manifest.csv
```

**Example Output** (compatible with amazon-s3-tar-tool):

```csv
Bucket,Key,Content-Length
my-bucket-name,folder1/file1.txt,1024
my-bucket-name,folder1/file2.txt,2048
my-bucket-name,folder2/file3.txt,512
```

### 2. Running S3Tar Operations

Execute amazon-s3-tar-tool commands on manifest files using the `run-s3tar.py` script:

```bash
# Basic usage with required destination bucket
uv run python src/s3_tar_helper/run-s3tar.py --dest-bucket my-destination-bucket

# Using the installed command-line tool (alternative)
uv run run-s3tar --dest-bucket my-destination-bucket

# Custom manifest directory and s3tar path
uv run python src/s3_tar_helper/run-s3tar.py \
  --manifest-dir /path/to/manifests \
  --dest-bucket my-destination-bucket \
  --s3tar-path /usr/local/bin/s3tar \
  --region us-west-2
```

**Parameters**:

- `--manifest-dir`: Directory containing CSV manifest files (default: `/home/ec2-user/data/manifests`)
- `--dest-bucket`: **Required** - Destination S3 bucket for tar files
- `--s3tar-path`: Path to amazon-s3-tar-tool executable (default: `./s3tar`)
- `--region`: AWS region (default: from `AWS_REGION` env var, fallback to `us-east-2`)

### Complete Workflow Example

Here's how to use this helper with the amazon-s3-tar-tool:

```bash
# 1. Generate manifest for your source bucket
uv run python src/s3_tar_helper/create-s3-manifest.py my-source-bucket --output-file source-manifest.csv

# 2. Run s3tar to create the tarball
uv run python src/s3_tar_helper/run-s3tar.py \
  --manifest-dir . \
  --dest-bucket my-archive-bucket \
  --s3tar-path /usr/local/bin/s3tar

# 3. The resulting tarball will be available at:
# s3://my-archive-bucket/tars/source-manifest.tar
```

### Why Use `uv run`?

- **No virtual environment activation needed**: `uv run` automatically uses the project's virtual environment
- **Dependency management**: Automatically installs and manages all required dependencies
- **Consistent environment**: Ensures the same Python version and dependencies across different machines
- **Clean execution**: No need to manually activate/deactivate virtual environments

### Alternative Execution Methods

While `uv run` is recommended, you can also:

```bash
# Activate virtual environment manually
source .venv/bin/activate

# Then run scripts directly
python src/s3_tar_helper/create-s3-manifest.py my-bucket-name
python src/s3_tar_helper/run-s3tar.py --dest-bucket my-destination-bucket

# Deactivate when done
deactivate
```

## Configuration

### AWS Credentials

Ensure your AWS credentials are properly configured using one of these methods:

1. **AWS CLI**:

   ```bash
   aws configure
   ```

2. **Environment Variables**:

   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_REGION=us-east-1
   ```

3. **IAM Roles** (for EC2 instances)

### Amazon S3 Tar Tool Installation

Install the amazon-s3-tar-tool for tar operations:

```bash
# Download and install amazon-s3-tar-tool
curl -L https://github.com/awslabs/amazon-s3-tar-tool/releases/latest/download/s3tar -o s3tar
chmod +x s3tar
sudo mv s3tar /usr/local/bin/
```

**Note**: The amazon-s3-tar-tool requires specific AWS permissions. See the [official documentation](https://github.com/awslabs/amazon-s3-tar-tool) for detailed IAM policy requirements.

## Development

### Code Quality Setup

This project uses pre-commit hooks to ensure code quality. The following tools are configured:

- **pre-commit**: Git hooks for automated code quality checks
- **ruff**: Fast Python linter and formatter
- **bandit**: Security linting
- **mypy**: Static type checking

### Setting Up Pre-commit

1. **Install development dependencies**:

   ```bash
   uv sync --group dev
   ```

2. **Install pre-commit hooks**:

   ```bash
   pre-commit install
   ```

3. **Run pre-commit on all files** (optional):

   ```bash
   pre-commit run --all-files
   ```

### Development Dependencies

The project includes development dependencies for code quality:

- **pre-commit**: Git hooks for code quality
- **ruff**: Fast Python linter and formatter
- **bandit**: Security linting
- **mypy**: Static type checking
- **types-requests**: Type stubs for requests library

To install development dependencies:

```bash
uv sync --group dev
```

### Code Quality Tools

#### Ruff (Linting and Formatting)

```bash
# Format code
uv run ruff format src/

# Lint code
uv run ruff check src/

# Fix auto-fixable issues
uv run ruff check --fix src/
```

#### Bandit (Security)

```bash
# Run security checks
uv run bandit -r src/
```

#### MyPy (Type Checking)

```bash
# Run type checking
uv run mypy src/
```

### Adding Dependencies

To add new dependencies:

1. **Add to pyproject.toml**:

   ```toml
   [project]
   dependencies = [
       "boto3>=1.38.45",
       "new-package>=1.0.0",
   ]
   ```

2. **Sync with UV**:
   ```bash
   uv sync
   ```

### Running Scripts in Development

```bash
# Activate virtual environment
source .venv/bin/activate

# Run scripts directly
python src/s3_tar_helper/create-s3-manifest.py my-bucket

# Or use UV run (recommended)
uv run python src/s3_tar_helper/create-s3-manifest.py my-bucket

# Or use installed scripts
uv run create-manifests my-bucket
uv run run-s3tar --dest-bucket my-destination-bucket
```

### Pre-commit Workflow

Once pre-commit is installed, it will automatically run on every commit. The hooks will:

1. **Format code** with ruff
2. **Lint code** for style and quality issues
3. **Check for security issues** with bandit
4. **Verify type annotations** with mypy
5. **Fix common issues** automatically

If any hooks fail, the commit will be blocked until the issues are resolved.

## Error Handling

The scripts include comprehensive error handling for common AWS S3 issues:

- **NoSuchBucket**: Bucket doesn't exist
- **AccessDenied**: Insufficient permissions
- **Empty Buckets**: No objects found
- **Network Issues**: Connection problems

## Examples

### Complete Workflow

1. **Create manifest for source bucket**:

   ```bash
   uv run python src/s3_tar_helper/create-s3-manifest.py source-bucket --output-file source-manifest.csv
   ```

2. **Run s3tar to create tar file**:
   ```bash
   uv run python src/s3_tar_helper/run-s3tar.py \
     --manifest-dir . \
     --dest-bucket destination-bucket \
     --s3tar-path /usr/local/bin/s3tar
   ```

### Batch Processing Multiple Buckets

```bash
# Create manifests for multiple buckets
for bucket in bucket1 bucket2 bucket3; do
  uv run python src/s3_tar_helper/create-s3-manifest.py $bucket --output-file ${bucket}-manifest.csv
done

# Process all manifests
uv run python src/s3_tar_helper/run-s3tar.py \
  --manifest-dir . \
  --dest-bucket archive-bucket
```

## Troubleshooting

### Common Issues

1. **Permission Denied**:

   - Verify AWS credentials and permissions
   - Check bucket access policies

2. **S3Tar Not Found**:

   - Ensure s3tar is installed and in PATH
   - Use `--s3tar-path` to specify custom location

3. **Python Version Issues**:
   - Ensure Python 3.13+ is installed
   - UV will automatically use the correct version

### Debug Mode

For troubleshooting, you can add debug output to the scripts or check AWS CloudTrail logs for detailed API calls.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with UV: `uv run python src/s3_tar_helper/your-script.py`
5. Submit a pull request

## License

[Add your license information here]

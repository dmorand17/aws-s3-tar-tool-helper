# 📦 AWS S3 Tar Helper

A Python helper project for working with the [amazon-s3-tar-tool](https://github.com/awslabs/amazon-s3-tar-tool) to create S3 bucket manifests and automate s3tar operations. This project provides complementary tools to generate CSV manifests of S3 bucket contents and execute s3tar commands for bulk operations.

## 📝 Overview

The [amazon-s3-tar-tool](https://github.com/awslabs/amazon-s3-tar-tool) is a powerful Go-based utility that creates tarballs of existing objects in Amazon S3 using multipart uploads. This helper project extends its functionality by providing:

- **Automated manifest generation**: Create CSV manifests of S3 bucket contents for use with s3tar
- **Batch processing**: Run s3tar operations across multiple manifest files
- **Python-based workflow**: Easy integration with Python-based data processing pipelines

## ⚙️ How It Works

1. **Generate Manifests**: Use this helper to create CSV manifests of your S3 bucket contents
2. **Process with s3tar**: Feed the manifests to the amazon-s3-tar-tool to create tarballs
3. **Automate Workflows**: Batch process multiple buckets or directories

## ✨ Features

- **S3 Manifest Creation**: Generate CSV manifests of S3 bucket contents with bucket, key, and content-length information
- **S3Tar Integration**: Run s3tar commands on manifest files for bulk S3 operations
- **UV Integration**: Modern Python dependency management with UV
- **Command Line Tools**: Installable scripts for easy command-line access
- **Batch Processing**: Process multiple manifest files automatically

## 🧰 Prerequisites

- Python 3.13+ (as specified in `.python-version`)
- [UV](https://docs.astral.sh/uv/) - Fast Python package installer and resolver
- AWS credentials configured (via AWS CLI, environment variables, or IAM roles)
- [amazon-s3-tar-tool](https://github.com/awslabs/amazon-s3-tar-tool) - The main s3tar executable

## 💾 Installation

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

   The easiest way is to use the provided helper script:

   ```bash
   bash download-s3tar.sh
   ```

   This will automatically download the latest compatible release and install it to `$HOME/.local/bin`.

   **Manual method:**

   ```bash
   # Download the latest release (example for Linux amd64)
   curl -L https://github.com/awslabs/amazon-s3-tar-tool/releases/latest/download/s3tar-linux-amd64.zip -o s3tar.zip
   unzip s3tar.zip
   chmod +x s3tar
   mv s3tar $HOME/.local/bin
   ```

   Make sure `$HOME/.local/bin` is in your `PATH`.

## 🚀 Usage

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

## 🛠️ Configuration

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

## 👩‍💻 Development

### Code Quality Setup

This project uses pre-commit hooks to ensure code quality. The following tools are configured:

- **pre-commit**: Git hooks for automated code quality checks
- **ruff**: Fast Python linter and formatter

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

## 📚 Examples

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with UV: `uv run python src/s3_tar_helper/your-script.py`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# EML Email Extractor

A Python script to quickly extract email addresses and associated names from `.eml` files. It scans both the email headers (To, From, CC, BCC, Reply-To) and the email body to find all unique email addresses and saves them to a CSV file.

## Features
- Extracts emails and names from standard email headers.
- Uses regex to find any email addresses scattered in the plain text or HTML body.
- Outputs a clean, deduplicated CSV file.
- Works on a single `.eml` file or an entire directory of `.eml` files.

## Prerequisites
- Python 3.x
- No external libraries required (uses only standard library modules).

## Usage

You can run the script directly from your terminal.

```bash
# Process all .eml files in the current directory
python main.py

# Process a specific .eml file
python main.py path/to/email.eml

# Process a specific directory containing .eml files
python main.py path/to/directory/

# Specify a custom output CSV filename using -o or --output
python main.py path/to/email.eml -o my_results.csv
```

### Help Command
Use the `-h` or `--help` flag to see all available options:
```bash
python main.py --help
```

## Output
The script generates a CSV file (default: `extracted_emails.csv`) with the following structure:
| Name | Email Address |
| :--- | :--- |
| John Doe | john.doe@example.com |
| N/A | no-name-found@example.com |
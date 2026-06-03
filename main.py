import os
import re
import email
from email import policy
import email.utils
import csv
import argparse

def process_eml_file(filepath, extracted_data):
    """
    Parses a single .eml file and extracts email addresses from headers and body.
    Updates the extracted_data dictionary in place.
    """
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    
    try:
        with open(filepath, 'rb') as f:
            # Parse the .eml file
            msg = email.message_from_binary_file(f, policy=policy.default)
            
            # 1. Extract from standard headers
            for header in ['from', 'to', 'cc', 'bcc', 'reply-to']:
                header_value = msg.get_all(header, [])
                for val in header_value:
                    # Use email.utils to properly parse header email addresses and names
                    addresses = email.utils.getaddresses([val])
                    for name, addr in addresses:
                        if addr:
                            addr_lower = addr.lower()
                            # Update name if we found a better one
                            if addr_lower not in extracted_data or (name and not extracted_data[addr_lower]):
                                extracted_data[addr_lower] = name.strip()
            
            # 2. Extract from the email body
            for part in msg.walk():
                if part.get_content_type() in ['text/plain', 'text/html']:
                    try:
                        payload = part.get_content()
                        if payload:
                            found_emails = email_pattern.findall(payload)
                            for found_email in found_emails:
                                addr_lower = found_email.lower()
                                if addr_lower not in extracted_data:
                                    extracted_data[addr_lower] = "" # No name found in body
                    except Exception as e:
                        print(f"Warning: Could not read a part of {filepath}: {e}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def extract_emails(path):
    """
    Extracts emails from a single .eml file or a directory of .eml files.
    Returns a dictionary mapping email addresses to names.
    """
    extracted_data = {}
    
    if os.path.isfile(path):
        if path.endswith('.eml'):
            process_eml_file(path, extracted_data)
        else:
            print(f"Error: The file '{path}' is not a .eml file.")
    elif os.path.isdir(path):
        eml_files = [f for f in os.listdir(path) if f.endswith('.eml')]
        if not eml_files:
            print(f"No .eml files found in directory '{path}'.")
        for filename in eml_files:
            filepath = os.path.join(path, filename)
            process_eml_file(filepath, extracted_data)
    else:
        print(f"Error: The path '{path}' does not exist.")
        
    return extracted_data

def main():
    parser = argparse.ArgumentParser(
        description="Extract email addresses from .eml files and save them to a CSV.",
        epilog="Example usage:\n  python main.py my_email.eml\n  python main.py my_folder/\n  python main.py -o results.csv my_folder/",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # Path argument (file or directory)
    parser.add_argument(
        'path', 
        nargs='?', 
        default='.', 
        help="Path to a single .eml file or a directory containing .eml files. Defaults to current directory."
    )
    
    # Output file argument
    parser.add_argument(
        '-o', '--output', 
        default='extracted_emails.csv', 
        help="Output CSV filename. Defaults to 'extracted_emails.csv'."
    )
    
    args = parser.parse_args()
    
    print(f"Scanning '{args.path}'...")
    email_data = extract_emails(args.path)
    
    if not email_data:
        print("No data extracted. Exiting.")
        return
        
    print(f"Found {len(email_data)} unique email addresses.")
    
    try:
        with open(args.output, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            # Write header
            writer.writerow(['Name', 'Email Address'])
            
            for email_addr, name in sorted(email_data.items(), key=lambda item: item[0]):
                display_name = name if name else "N/A"
                writer.writerow([display_name, email_addr])
                
        print(f"Data successfully saved to '{args.output}'.")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

if __name__ == '__main__':
    main()

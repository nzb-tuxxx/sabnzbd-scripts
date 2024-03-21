
# ebook2kindle.py - Kindle eBook Delivery Script for SABnzbd

## Overview

This Python script automates the delivery of downloaded eBooks to an Amazon Kindle device directly from SABnzbd. It filters the downloaded content by predefined eBook formats and categories, then sends the files to the specified Kindle email addresses configured in the `settings.ini` file.

## Features

- **SMTP Email Sending**: Configurable SMTP server settings for email delivery.
- **Category-Based Email Mapping**: Define Kindle email addresses based on download categories.
- **Preferred eBook Formats**: Filters attachments by preferred eBook file formats (e.g., epub, mobi).
- **Default Kindle Address**: Sends eBooks to a default Kindle email if no category match is found.
- **Optional BCC**: Ability to send a blind copy to another email address for tracking.

## Configuration

Before using the script, configure the `ebook2kindle.ini` file with your SMTP server details, Kindle email addresses, and preferred eBook formats.

Example `ebook2kindle.ini`:

```ini
[smtp]
server = smtp.example.com
port = 587
username = user@example.com
password = yourpassword

[email]
from = your-email@example.com
bcc = optional-bcc-email@example.com
default_receiver = your-kindle-email@kindle.com

[category_mapping]
ebooks = your-kindle-email@kindle.com
ebooks-mommy = another-kindle-email@kindle.com

[preferences]
preferred_types = epub, azw
```

## Usage

1. Place the script and the `ebook2kindle.ini` file in your SABnzbd scripts directory and make the script executable.
2. Configure SABnzbd to use this script as a post-processing script for your eBook categories.
3. Make sure that you allowed sending eBook from your specified email to your kindle in your amazon account settings.
4. Enjoy automatic eBook delivery to your Kindle!

## Requirements

- Python 3.x
- SABnzbd

## License

MIT



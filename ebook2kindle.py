#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ebook2kindle.py - Kindle eBook Delivery Script for SABnzbd

Usage:
- Configure as a post-processing script in SABnzbd
- Ensure 'ebook2kindle.ini' is set up in the same directory as this script
- Customize the 'ebook2kindle.ini' file as per your requirements
- Make ebook2kindle.py executable

Requirements:
- Python 3.x
- A correctly configured 'ebook2kindle.ini' file.

Author: nzb-tuxxx
Version: 0.1
URL: https://github.com/nzb-tuxxx/sabnzbd-scripts
"""

import configparser
import fnmatch
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def read_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'ebook2kindle.ini')

    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(config_path)

    if not config.sections():
        print(f"Config {config_path} is invalid")
        sys.exit(1)

    mandatory_settings = ['server', 'port', 'username', 'password', 'from', 'default_receiver']
    for setting in mandatory_settings:
        if setting not in config['smtp'] and setting not in config['email']:
            print(f"Mandatory setting '{setting}' is missing. Please update the ebook2kindle.ini.example file.")
            sys.exit(1)

    preferred_types = config['preferences'].get('preferred_types', 'epub, azw').split(', ')

    return {
        'smtp_server': config['smtp']['server'],
        'smtp_port': config['smtp'].getint('port'),
        'smtp_username': config['smtp']['username'],
        'smtp_password': config['smtp']['password'],
        'email_from': config['email']['from'],
        'email_bcc': config['email'].get('bcc'),
        'default_receiver': config['email']['default_receiver'],
        'category_email_mapping': dict(config.items('category_mapping')),
        'preferred_types': preferred_types
    }


def find_files(folder_path, patterns):
    all_files = []
    for root, dirs, files in os.walk(folder_path):
        for pattern in patterns:
            for filename in fnmatch.filter(files, f"*.{pattern}"):
                all_files.append(os.path.join(root, filename))
    return all_files


def select_files(all_files, preferred_types):
    selected_files = []
    for file in all_files:
        for ext in preferred_types:
            if file.lower().endswith(f".{ext.lower()}"):
                selected_files.append(file)
                break
    return selected_files


def send_email(config, selected_files, folder_path, email_receiver):
    msg = MIMEMultipart()
    msg["Subject"] = f"[ebook2kindle] New E-Book {os.path.basename(folder_path)}"
    msg["From"] = config['email_from']
    msg["To"] = email_receiver
    if config['email_bcc']:
        msg["Bcc"] = config['email_bcc']

    text_msg = MIMEText("Attached are the selected ebooks found in the folder.")
    msg.attach(text_msg)

    for file in selected_files:
        with open(file, "rb") as f:
            file_content = f.read()
            file_name = os.path.basename(file)
            mime_app = MIMEApplication(file_content, Name=file_name)
            mime_app.add_header('Content-Disposition', 'attachment', filename=file_name)
            msg.attach(mime_app)

    with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
        server.starttls()
        server.login(config['smtp_username'], config['smtp_password'])
        recipients = [email_receiver] + [config['email_bcc']] if config['email_bcc'] else [email_receiver]
        server.sendmail(config['email_from'], recipients, msg.as_string())


def main():
    config = read_config()
    try:
        (scriptname, folder_path, orgnzbname, jobname, reportnumber, category, group, postprocstatus, url) = sys.argv
    except:
        print("No commandline parameters found")
        sys.exit(1)

    email_receiver = config['category_email_mapping'].get(category, config['default_receiver'])

    all_files = find_files(folder_path, config['preferred_types'])
    selected_files = select_files(all_files, config['preferred_types'])

    if selected_files:
        send_email(config, selected_files, folder_path, email_receiver)
        print(f"Sent mail to {email_receiver}")
    else:
        print("No preferred files found.")


if __name__ == "__main__":
    main()

import os
import time
import subprocess
import requests
import email
import imaplib

# --- Directories ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ORDERS_DIR = os.path.join(BASE_DIR, "orders")
CONFIG_FILE = os.path.join(BASE_DIR, "config.ini")

# Make sure orders folder exists
os.makedirs(ORDERS_DIR, exist_ok=True)

# --- Environment Variables (set in Koyeb Dashboard) ---
EMAIL_HOST = os.getenv("EMAIL_HOST", "imap.gmail.com")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
LIVE_MODE = os.getenv("LIVE_MODE", "false").lower() == "true"
PRINTER_API_URL = os.getenv("PRINTER_API_URL")
PRINTER_API_KEY = os.getenv("PRINTER_API_KEY")

# Path to PrusaSlicer inside Docker (you’ll update this later if needed)
PRUSASLICER_EXE = "prusa-slicer"

# --- Email check function ---
def check_email_for_orders():
    print("Checking email for new orders...")
    try:
        mail = imaplib.IMAP4_SSL(EMAIL_HOST)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")
        result, data = mail.search(None, "UNSEEN")
        if result != "OK":
            return []

        orders = []
        for num in data[0].split():
            result, msg_data = mail.fetch(num, "(RFC822)")
            if result != "OK":
                continue
            raw_msg = msg_data[0][1]
            msg = email.message_from_bytes(raw_msg)
            subject = msg["subject"]
            print(f"📩 New email: {subject}")
            # In a real setup, parse attachments here
            orders.append(subject)
        return orders
    except Exception as e:
        print("Email check failed:", e)
        return []

# --- Slicing function ---
def slice_model(order_folder):
    stl_file = os.path.join(order_folder, "model.stl")
    gcode_file = os.path.join(or_


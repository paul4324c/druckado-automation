import os
import time
import requests
import pyzmail36
import subprocess

# =============================
# CONFIGURATION (Environment Variables)
# =============================
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
LIVE_MODE = os.environ.get("LIVE_MODE", "false").lower() == "true"
PRINTER_API_URL = os.environ.get("PRINTER_API_URL")
PRINTER_API_KEY = os.environ.get("PRINTER_API_KEY")

# Path where orders will be temporarily stored
ORDERS_DIR = "/app/orders"

# PrusaSlicer executable path inside Docker
PRUSASLICER_EXE = "/usr/bin/prusa-slicer"  # Adjust if using custom Docker image


# =============================
# FUNCTIONS
# =============================
def check_email():
    """Check inbox for new order emails and download attachments"""
    orders_found = []
    try:
        from imapclient import IMAPClient
    except ImportError:
        print("IMAPClient not installed. Make sure requirements.txt has it.")
        return orders_found

    with IMAPClient(EMAIL_HOST) as client:
        client.login(EMAIL_USER, EMAIL_PASS)
        client.select_folder("INBOX")
        messages = client.search(["UNSEEN"])
        for msgid, data in client.fetch(messages, ["BODY[]"]).items():
            msg = pyzmail36.PyzMessage.factory(data[b"BODY[]"])
            subject = msg.get_subject()
            if msg.text_part:
                body = msg.text_part.get_payload().decode(msg.text_part.charset)
            else:
                body = ""
            print(f"📩 New order detected: {subject}")
            # Save STL attachment
            for part in msg.mailparts:
                if part.filename and part.filename.lower().endswith(".stl"):
                    order_folder = os.path.join(ORDERS_DIR, f"order_{msgid}")
                    os.makedirs(order_folder, exist_ok=True)
                    file_path = os.path.join(order_folder, part.filename)
                    with open(file_path, "wb") as f:
                        f.write(part.get_payload())
                    orders_found.append(order_folder)
    return orders_found


def slice_model(order_folder):
    """Simulate slicing STL files into G-code"""
    for file in os.listdir(order_folder):
        if file.lower().endswith(".stl"):
            stl_file = os.path.join(order_folder, file)
            gcode_file = os.path.join(order_folder, "model.gcode")
            print(f"Slicing {stl_file} -> {gcode_file}")
            # Use subprocess to call PrusaSlicer CLI
            # Replace PRUSASLICER_EXE with your executable path if needed
            subprocess.run([
                PRUSASLICER_EXE,
                "--load", "/app/config.ini",  # your slicer config
                "--output", gcode_file,
                stl_file
            ])
            print(f"✅ Sliced: {gcode_file}")
            return gcode_file
    return None


def send_to_printer(gcode_file):
    """Send G-code to printer if LIVE_MODE is True"""
    if not LIVE_MODE:
        print(f"[SIMULATION] Would send {gcode_file} to printer")
        return
    if not PRINTER_API_URL or not PRINTER_API_KEY:
        print("Printer API info missing. Cannot send G-code.")
        return
    with open(gcode_file, "rb") as f:
        files = {"file": f}
        headers = {"Authorization": f"Bearer {PRINTER_API_KEY}"}
        response = requests.post(PRINTER_API_URL, files=files, headers=headers)
        if response.status_code == 200:
            print(f"✅ Successfully sent {gcode_file} to printer")
        else:
            print(f"❌ Failed to send {gcode_file}: {response.text}")


def process_orders():
    """Full pipeline: check email → slice → send"""
    orders = check_email()
    for order_folder in orders:
        gcode_file = slice_model(order_folder)
        if gcode_file:
            send_to_printer(gcode_file)


# =============================
# MAIN LOOP
# =============================
if __name__ == "__main__":
    print("🚀 Druckado Automation Worker started")
    while True:
        try:
            process_orders()
            print("Waiting 60 seconds before checking for new orders...")
            time.sleep(60)
        except Exception as e:
            print(f"⚠️ Error occurred: {e}")
            time.sleep(60)

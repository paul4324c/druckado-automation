import os
import time
import requests
import pyzmail36

# =============================
# CONFIGURATION (Environment Variables)
# =============================
EMAIL_HOST = os.environ.get("EMAIL_HOST")       # e.g. imap.gmail.com
EMAIL_USER = os.environ.get("EMAIL_USER")       # test inbox email
EMAIL_PASS = os.environ.get("EMAIL_PASS")       # app password or mailbox password

LIVE_MODE = os.environ.get("LIVE_MODE", "false").lower() == "true"
PRINTER_API_URL = os.environ.get("PRINTER_API_URL", "https://httpbin.org/post")
PRINTER_API_KEY = os.environ.get("PRINTER_API_KEY", "DUMMY_KEY")

# Path where orders will be temporarily stored
ORDERS_DIR = "/app/orders"

# =============================
# FUNCTIONS
# =============================
def check_email():
    """Check inbox for new order emails and download STL attachments."""
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
            print(f"📩 New order detected: {subject}")
            
            # Save STL attachments
            for part in msg.mailparts:
                if part.filename and part.filename.lower().endswith(".stl"):
                    order_folder = os.path.join(ORDERS_DIR, f"order_{msgid}")
                    os.makedirs(order_folder, exist_ok=True)
                    file_path = os.path.join(order_folder, part.filename)
                    with open(file_path, "wb") as f:
                        f.write(part.get_payload())
                    print(f"📂 Saved STL to {file_path}")
                    orders_found.append(order_folder)
    return orders_found


def slice_model(order_folder):
    """Simulate slicing STL to G-code."""
    for file in os.listdir(order_folder):
        if file.lower().endswith(".stl"):
            stl_file = os.path.join(order_folder, file)
            gcode_file = os.path.join(order_folder, "model.gcode")
            print(f"🛠️ Slicing {stl_file} -> {gcode_file}")
            
            # Fake G-code file for testing
            with open(gcode_file, "w") as f:
                f.write("; G-code placeholder\n")
            print(f"✅ Created dummy G-code at {gcode_file}")
            return gcode_file
    return None


def send_to_printer(gcode_file):
    """Send (or simulate sending) G-code to printer."""
    if not LIVE_MODE:
        print(f"[SIMULATION] Would send {gcode_file} to printer at {PRINTER_API_URL}")
        # Optional "echo" test using httpbin
        with open(gcode_file, "rb") as f:
            test_resp = requests.post("https://httpbin.org/post", files={"file": f})
            print("🌐 Test echo response from httpbin:", test_resp.json()["files"])
        return

    if not PRINTER_API_URL or not PRINTER_API_KEY:
        print("❌ Missing printer API info. Cannot send G-code.")
        return

    headers = {"Authorization": f"Bearer {PRINTER_API_KEY}"}
    with open(gcode_file, "rb") as f:
        files = {"file": (os.path.basename(gcode_file), f, "application/octet-stream")}
        response = requests.post(PRINTER_API_URL, 

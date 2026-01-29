import qrcode
import os

# create folder if not exists
os.makedirs("qr_codes", exist_ok=True)

# list of fitting IDs
fitting_ids = [
    "RF-ERC-2024-000187",
    "RF-ERC-2024-000188",
    "RF-ERC-2024-000189"
]

for fid in fitting_ids:
    qr = qrcode.make(fid)
    file_path = f"qr_codes/{fid}.png"
    qr.save(file_path)
    print(f"QR code generated: {file_path}")

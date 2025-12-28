#!/bin/bash

echo "[*] Installing PhoneSpectre..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[-] Python3 not found"
    exit 1
fi

# Install dependencies
pip3 install phonenumbers colorama --quiet

# Install tool
sudo cp phonespectre.py /usr/bin/phonespectre
sudo chmod +x /usr/bin/phonespectre

echo "[+] PhoneSpectre installed successfully"
echo "[+] Run: phonespectre +14155552671"

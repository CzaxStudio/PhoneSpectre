#!/usr/bin/env python3
# PhoneSpectre - Legal Phone Number OSINT Tool for Kali Linux

import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from colorama import Fore, Style, init
import argparse
import json
import sys
import os

init(autoreset=True)

VERSION = "1.2"

def banner():
    print(Fore.RED + r"""
██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗███████╗
██╔══██╗██║  ██║██╔═══██╗████╗  ██║██╔════╝
██████╔╝███████║██║   ██║██╔██╗ ██║█████╗  
██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║██╔══╝  
██║     ██║  ██║╚██████╔╝██║ ╚████║███████╗
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
""" + Style.BRIGHT + f"PhoneSpectre v{VERSION} | Legal OSINT Tool\n")

def spam_risk(parsed):
    risk = 0
    if not carrier.name_for_number(parsed, "en"):
        risk += 1
    if phonenumbers.number_type(parsed) == phonenumbers.PhoneNumberType.VOIP:
        risk += 2
    return "Low" if risk == 0 else "Medium" if risk == 1 else "High"

def analyze(number, export=None, silent=False):
    try:
        parsed = phonenumbers.parse(number)
    except:
        print(Fore.RED + " Invalid phone number format")
        return

    e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    international = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

    data = {
        "input": number,
        "valid": phonenumbers.is_valid_number(parsed),
        "possible": phonenumbers.is_possible_number(parsed),
        "country": geocoder.description_for_number(parsed, "en"),
        "carrier": carrier.name_for_number(parsed, "en") or "Unknown",
        "timezone": list(timezone.time_zones_for_number(parsed)),
        "international": international,
        "e164": e164,
        "country_code": parsed.country_code,
        "line_type": phonenumbers.number_type(parsed),
        "spam_risk": spam_risk(parsed),
        "social_checks": {
            "WhatsApp": f"https://wa.me/{e164[1:]}" if phonenumbers.is_valid_number(parsed) else None,
            "Telegram": "Manual search recommended",
            "Truecaller": "Manual search recommended"
        }
    }

    if not silent:
        print(Fore.CYAN + "\n PhoneSpectre OSINT Report")
        print(Fore.YELLOW + "-" * 45)
        for k, v in data.items():
            if k != "social_checks":
                print(Fore.GREEN + f"{k.replace('_',' ').title():18}: {v}")
        print(Fore.YELLOW + "-" * 45)
        print(Fore.CYAN + " Social Presence Hints:")
        for k, v in data["social_checks"].items():
            print(Fore.GREEN + f"  {k}: {v}")
        print(Fore.YELLOW + "-" * 45)
        print(Fore.CYAN + " Public OSINT only. No tracking performed.\n")

    if export:
        with open(export, "w") as f:
            json.dump(data, f, indent=4)
        print(Fore.GREEN + f" Report exported to {export}")


    if not silent:
        print(Fore.CYAN + "\n PhoneSpectre OSINT Report")
        print(Fore.YELLOW + "-" * 45)
        for k, v in data.items():
            if k != "social_checks":
                print(Fore.GREEN + f"{k.replace('_',' ').title():18}: {v}")
        print(Fore.YELLOW + "-" * 45)
        print(Fore.CYAN + " Social Presence Hints:")
        for k, v in data["social_checks"].items():
            print(Fore.GREEN + f"  {k}: {v}")
        print(Fore.YELLOW + "-" * 45)
        print(Fore.CYAN + " Public data only. No tracking performed.\n")

    if export:
        with open(export, "w") as f:
            json.dump(data, f, indent=4)
        print(Fore.GREEN + f" Report exported to {export}")

def main():
    parser = argparse.ArgumentParser(
        description="PhoneSpectre - Legal Phone Number OSINT Tool (Kali Linux)",
        usage="phonespectre +14155552671 [options]"
    )

    parser.add_argument("number", help="Target phone number with country code")
    parser.add_argument("-o", "--output", help="Export report to JSON file")
    parser.add_argument("-s", "--silent", action="store_true", help="Silent mode (no banner/output)")
    parser.add_argument("-v", "--version", action="store_true", help="Show version")

    args = parser.parse_args()

    if args.version:
        print("PhoneSpectre version", VERSION)
        sys.exit(0)

    if not args.silent:
        banner()

    analyze(args.number, export=args.output, silent=args.silent)

if __name__ == "__main__":
    main()

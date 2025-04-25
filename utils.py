import ipaddress
import os
import re
import socket

from datetime import datetime
from logger import Log
from urllib.parse import urlparse, urlunparse

DEBUG_DIR = "debug"

def screenshot_filename(prefix: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.png"

async def take_screenshot(page, label: str):
    try:
        os.makedirs(DEBUG_DIR, exist_ok=True)
        filename = screenshot_filename(label)
        path = os.path.join(DEBUG_DIR, filename)
        await page.screenshot(path=path, full_page=True)
        Log.debug(f"Screenshot saved: {path}")
    except Exception as e:
        Log.error(f"Screenshot failed: {e}")

def normalize_url(user_input: str) -> str:
    user_input = user_input.strip()

    # Add https:// if scheme is missing
    if not user_input.startswith(("http://", "https://")):
        user_input = "https://" + user_input

    parsed = urlparse(user_input)

    # Reject unsupported schemes
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Invalid URL scheme. Only 'http' or 'https' are allowed.")

    # Fallback: if netloc is missing, try using path as domain
    netloc = parsed.netloc or parsed.path
    if not netloc:
        raise ValueError("Invalid URL. Example of a valid URL: 'https://www.amazon.com'")

    # Check if it's an IP — don't prepend www or validate domain pattern
    try:
        ipaddress.ip_address(netloc.split(':')[0])
        is_ip = True
    except ValueError:
        is_ip = False

    if not is_ip:
        # Extract host without port for validation
        host_only = netloc.split(':')[0]

        domain_pattern = r"^[a-zA-Z0-9.-]+\.[a-z]{2,}$"
        if not re.match(domain_pattern, host_only):
            raise ValueError("Invalid URL. Example of a valid URL: 'https://www.amazon.com'")

    # Final normalized URL
    normalized_url = urlunparse(("https", netloc, "", "", "", ""))
    
    # Check if domain actually resolves
    if not domain_resolves(host_only):
        raise ValueError(f"Hmm, we could not find '{netloc}'. Please check that the address is correct.")

    return normalized_url

def domain_resolves(domain: str) -> bool:
    try:
        socket.gethostbyname(domain)
        return True
    except socket.error:
        return False

async def navigate_to_url(page, url, debug=False):
    Log.info(f"Opening URL: {url}")
    try:
        await page.goto(url)
        return True
    except Exception as e:
        if debug:
            Log.debug(f"Error while loading {url}: {e}")
        Log.error("Error: Could not load the page. Please check the URL or try again later.")
        await take_screenshot(page, "load_fail")
        return False

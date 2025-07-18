import re
import requests
from bs4 import BeautifulSoup
from .models import ContactInfo, BrandData

def fetch_website(url: str) -> BeautifulSoup:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def extract_emails(text: str) -> list:
    return list(set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)))

def extract_phones(text: str) -> list:
    return list(set(re.findall(r"\+?\d[\d\s\-\(\)]{7,}\d", text)))

def extract_contact_details(soup: BeautifulSoup) -> ContactInfo:
    text = soup.get_text()
    return ContactInfo(
        emails=extract_emails(text),
        phone_numbers=extract_phones(text)
    )

def extract_brand_data(url: str) -> BrandData:
    soup = fetch_website(url)
    title = soup.title.string.strip() if soup.title else "No Title Found"
    desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
    description = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else "No Description Found"
    logo_tag = soup.find("link", rel="icon") or soup.find("link", rel="shortcut icon")
    logo = logo_tag["href"] if logo_tag and logo_tag.get("href") else ""

    if logo and not logo.startswith("http"):
        logo = url.rstrip("/") + "/" + logo.lstrip("/")

    contact_info = extract_contact_details(soup)

    return BrandData(
        title=title,
        description=description,
        logo=logo,
        contact_details=contact_info
    )

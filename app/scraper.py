import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

def get_full_url(base, path):
    return urljoin(base, path)

def get_products(base_url):
    try:
        res = requests.get(get_full_url(base_url, "/products.json"), timeout=10)
        if res.status_code == 200:
            return res.json().get('products', [])
    except:
        return []
    return []

def extract_policy_text(base_url, keyword):
    try:
        res = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(res.text, 'lxml')
        for a in soup.find_all('a', href=True):
            if keyword in a['href'].lower():
                link = urljoin(base_url, a['href'])
                policy_res = requests.get(link)
                return BeautifulSoup(policy_res.text, 'lxml').get_text(separator="\n")
    except:
        return ""
    return ""

def extract_home_products(base_url):
    try:
        res = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(res.text, 'lxml')
        products = []
        for a in soup.find_all('a', href=True):
            if '/products/' in a['href']:
                products.append(urljoin(base_url, a['href']))
        return list(set(products))
    except:
        return []

def extract_faqs(base_url):
    try:
        res = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(res.text, 'lxml')
        faqs = []
        for section in soup.find_all(['details', 'div']):
            text = section.get_text(separator="\n")
            if "?" in text:
                qas = re.findall(r'(Q.*?)\n(A.*?)\n', text, re.DOTALL)
                for q, a in qas:
                    faqs.append({'question': q.strip(), 'answer': a.strip()})
        return faqs
    except:
        return []

def extract_socials(soup):
    links = { "instagram": "", "facebook": "", "tiktok": "", "twitter": "" }
    for a in soup.find_all('a', href=True):
        href = a['href']
        for key in links:
            if key in href:
                links[key] = href
    return links

def extract_contact_details(soup):
    text = soup.get_text()
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    phones = re.findall(r'\+?\d[\d -]{8,}\d', text)
    return list(set(emails)), list(set(phones))

def extract_about_and_links(base_url):
    try:
        res = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(res.text, 'lxml')
        about_text = ""
        for a in soup.find_all('a', href=True):
            if 'about' in a['href'].lower():
                link = urljoin(base_url, a['href'])
                about_res = requests.get(link)
                about_text = BeautifulSoup(about_res.text, 'lxml').get_text(separator="\n")
                break
        links = {}
        for a in soup.find_all('a', href=True):
            if any(x in a['href'].lower() for x in ['track', 'blog', 'contact']):
                links[a.get_text(strip=True)] = urljoin(base_url, a['href'])
        return about_text, links
    except:
        return "", {}

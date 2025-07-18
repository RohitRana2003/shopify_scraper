from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from app.scraper import (
    get_products,
    extract_home_products,
    extract_policy_text,
    extract_faqs,
    extract_socials,
    extract_contact_details,
    extract_about_and_links
)
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Enable CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scrape")
def scrape_shopify(website_url: str = Query(..., description="Shopify Store URL")):
    try:
        if not website_url.startswith("http"):
            website_url = "https://" + website_url

        res = requests.get(website_url, timeout=10)
        if res.status_code != 200:
            raise HTTPException(status_code=401, detail="Website not reachable")

        soup = BeautifulSoup(res.text, 'lxml')

        # Safely unpack contact and about details
        contact_emails, contact_phones = extract_contact_details(soup)
        about_text, important_links = extract_about_and_links(website_url)

        data = {
            "brand_url": website_url,
            "product_catalog": get_products(website_url),
            "hero_products": extract_home_products(website_url),
            "privacy_policy": extract_policy_text(website_url, "privacy"),
            "return_refund_policy": extract_policy_text(website_url, "refund"),
            "faqs": extract_faqs(website_url),
            "social_handles": extract_socials(soup),
            "contact_details": {
                "emails": contact_emails,
                "phones": contact_phones
            },
            "about_brand": about_text,
            "important_links": important_links
        }

        return {"status": "success", "data": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

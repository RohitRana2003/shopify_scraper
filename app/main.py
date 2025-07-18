from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from .scraper import extract_brand_data
from .models import BrandData

app = FastAPI()

@app.get("/scrape", response_model=BrandData)
def scrape_shopify_site(url: str = Query(..., description="Full URL of the Shopify site to scrape")):
    try:
        data = extract_brand_data(url)
        return data
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal Server Error: {str(e)}"}
        )

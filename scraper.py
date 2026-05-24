import requests
from bs4 import BeautifulSoup

def scrape_internshala(keyword):
    url = f"https://internshala.com/internships/{keyword}-internship"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    print("Page title:", soup.title.text if soup.title else "No title found")
    print("\nFirst 2000 characters of page:\n")
    print(soup.get_text()[:2000])

if __name__ == "__main__":
    print("Scraping AI/ML internships from Internshala...\n")
    scrape_internshala("machine-learning")
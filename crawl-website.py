import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json

# Function to check if the link is internal or external
def is_internal(url, domain):
  return urlparse(url).netloc == domain

# Function to crawl a website recursively and collect internal and external links
def crawl_website(start_url):
  visited = set()  # To avoid visiting the same URL multiple times
  internal_links = set()
  external_links = set()
  pdf_links = []
  domain = urlparse(start_url).netloc


  def crawl(url):
    # Skip already visited URLs
    if url in visited:
      return
    visited.add(url)

    try:
      response = requests.get(url)
      if response.status_code != 200:
        return
      soup = BeautifulSoup(response.text, 'html.parser')
      
      for link in soup.find_all('a', href=True):
        link_url = link['href']
        
        if "https" in link_url:
          if is_internal(link_url, domain):
            internal_links.add(link_url)
            # print(link_url)
            if link_url.find(".pdf") == -1:
              crawl(link_url)  # Recursively crawl internal links
            else:
              if link.get('target') == None or link.get('target').find("_blank") == -1:
                # print(url)
                # print(link_url)
                pdf_links.append({
                  'url': url,
                  'link': link_url
                  })
          else:
            external_links.add(link_url)
        
    except requests.exceptions.RequestException:
      return

  # Start crawling from the initial URL
  crawl(start_url)

  return list(internal_links), list(external_links), pdf_links

# Example usage:
if __name__ == '__main__':
  start_url = 'https://en.triton-am.com'  # Replace with the starting URL
  internal, external, pdf = crawl_website(start_url)
  
  # print("Internal Links:")
  # for link in internal:
  #   print(link)

  # print("\nExternal Links:")
  # for link in external:
  #   print(link)

  print("PDF Links:")
  url = "None"
  for link in pdf:
    if url != link['url']:
      print(link['url'])
    url = link['url']
    print(f"\t{link['link']}")


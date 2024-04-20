import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import sys

def get_top_urls(query, num_results=5):
    print(f"Fetching top URLs for the query: {query}")  # Debug statement
    search_url = "https://www.google.com/search"
    params = {"q": query}
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(search_url, params=params, headers=headers)
        response.raise_for_status()

        print(f"HTTP response status: {response.status_code}")  # Debug statement
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all('a', href=True)
        print(f"Number of links found: {len(links)}")  # Debug statement

        urls = []
        for link in links:
            href = link['href']
            if href.startswith('/url?q='):
                url = parse_qs(urlparse(href).query)['q'][0]
                urls.append(url)
                print(f"URL found: {url}")  # Debug statement
            if len(urls) >= num_results:
                break

        return urls
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def save_urls_to_file(urls, filename="urls.txt"):
    print(f"Saving URLs to file: {filename}")  # Debug statement
    with open(filename, 'w') as file:
        for url in urls:
            file.write(url + "\n")
    print(f"Saved {len(urls)} URLs.")  # Debug statement


if __name__ == "__main__":
    query = sys.argv[1]  # Take query from the first command line argument
    print(f"Script started with query: {query}")  # Debug statement
    top_urls = get_top_urls(query)
    save_urls_to_file(top_urls)
    with open('last_query.txt', 'w') as f:
        f.write(query)
    print("Script execution completed.")  # Debug statement
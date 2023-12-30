import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin

def get_top_urls(query, num_results=10):
    # Google search URL (Update as needed)
    search_url = "https://www.google.com/search"
    params = {"q": query}
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(search_url, params=params, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Find all the <a> tags
        links = soup.find_all('a', href=True)

        # Filter and clean the URLs
        urls = []
        for link in links:
            href = link['href']

            # Check if the URL is a Google redirect URL
            if href.startswith('/url?q='):
                # Parse the actual URL from the query string
                url = parse_qs(urlparse(href).query)['q'][0]
                urls.append(url)

            if len(urls) >= num_results:
                break

        return urls
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def save_urls_to_file(urls, filename="urls.txt"):
    with open(filename, 'w') as file:
        for url in urls:
            file.write(url + "\n")

if __name__ == "__main__":
    query = input("Enter your search query: ")
    top_urls = get_top_urls(query)
    save_urls_to_file(top_urls)

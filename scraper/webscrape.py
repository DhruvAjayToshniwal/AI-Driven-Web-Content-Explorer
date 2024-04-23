import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import sys

def get_top_urls(query, num_results=5):
    print(f"Fetching top URLs for the query: {query}")
    search_url = "https://www.google.com/search"
    params = {"q": query}
    headers = {"User-Agent": "Mozilla/5.0"}
    fetched_urls = []
    attempt_count = 0

    while len(fetched_urls) < num_results and attempt_count < 50:
        response = requests.get(search_url, params=params, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all('a', href=True)

        for link in links:
            href = link['href']
            if href.startswith('/url?q='):
                url = parse_qs(urlparse(href).query)['q'][0]
                if "youtube.com" not in url and "maps.google.com" not in url and not url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    fetched_urls.append(url)
                if len(fetched_urls) == num_results:
                    break

        params['start'] = attempt_count * 10
        attempt_count += 1

    print(f"Collected {len(fetched_urls)} URLs.")
    return fetched_urls

def save_urls_to_file(urls, filename="urls.txt"):
    with open(filename, 'w') as file:
        for url in urls:
            file.write(url + "\n")
    print(f"Saved URLs to {filename}")

if __name__ == "__main__":
    query = sys.argv[1]
    model = sys.argv[2]
    top_urls = get_top_urls(query)
    save_urls_to_file(top_urls)
    with open('last_query.txt', 'w') as f:
        f.write(query + "\n" + model)
    print("Script execution completed.")

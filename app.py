from flask import Flask, render_template, request, redirect, url_for
import subprocess
import os
import main
import requests

app = Flask(__name__)

def download_html_files(urls_file, output_dir):
    with open(urls_file, 'r') as file:
        urls = file.readlines()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for i, url in enumerate(urls):
        url = url.strip()
        if not any(x in url for x in ["youtube.com", "maps.google.com"]) and not url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            try:
                print(f"Downloading {url}...")
                response = requests.get(url)
                file_path = os.path.join(output_dir, f"document_{i}.html")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"Saved {file_path}")
            except requests.RequestException as e:
                print(f"Error downloading {url}: {e}")
            
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query = request.form['query']
        model = request.form['model']
        print(f"Received query from form: {query}, Model: {model}")
        return redirect(url_for('start_process', query=query, model=model))
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def start_process():
    query = request.form['query']
    model = request.form['model']
    print(f"Starting process for query: {query}")
    try:
        subprocess.run(['cleanup.bat'], shell=True, check=True)
        print("Cleanup completed.")

        subprocess.run(['python', 'scraper/webscrape.py', query, model], shell=True, check=True)
        print("Webscraping completed.")

        if not os.path.exists('websites'):
            os.makedirs('websites')
        if not os.path.isfile('urls.txt') or os.path.getsize('urls.txt') == 0:
            print("No URLs found.")
            return "No URLs found, exiting."

        download_html_files('urls.txt', 'websites')

        subprocess.run(['python', 'scraper/cleaner.py'], shell=True, check=True)
        print("Cleaning completed.")

        subprocess.run(['python', 'scraper/chunker.py'], shell=True, check=True)
        print("Chunking completed.")

        subprocess.run(['python', 'back-end/main.py'], shell=True, check=True)
        print("Main processing completed.")

        with open('output.txt', 'r') as file:
            answer = file.read()

        subprocess.run(['cleanup.bat'], shell=True, check=True)
        print("Cleanup completed.")
        
        return render_template('results.html', query=query, answer=answer)
    except subprocess.CalledProcessError as e:
        print(f"Error in processing: {e}")
        return f"An error occurred: {e}. Process stopped."

if __name__ == '__main__':
    app.run(debug=False)

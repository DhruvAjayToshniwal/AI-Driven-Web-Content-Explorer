# AI-Driven-Web-Content-Explorer

This project is designed to scrape, process, and analyze web content, delivering contextually relevant responses using OpenAI's GPT-3.5 Turbo model. It automates the collection of web articles based on user queries, processes the content for relevant information, and uses AI to generate insightful answers.

## Components Overview

### `chunker.py`

This script processes HTML files from a specified directory, extracting and chunking textual content. It uses BeautifulSoup for HTML parsing and the `tiktoken` tokenizer for splitting text into manageable segments.

### `cleaner.py`

Cleans downloaded HTML files by removing extraneous HTML tags and formatting the content. This script ensures that only relevant text is extracted for analysis.

### `webscrape.py`

Performs web scraping to fetch the top URLs based on a user's search query. It uses BeautifulSoup to parse Google search results and retrieves URLs for further downloading and processing.

### `vectorizer.py`

Creates and manages a vector database. It processes text data into embeddings using OpenAI's API and stores these embeddings for similarity searches.

### `main.py`

The main script for the project. It initiates an interactive conversational interface where users can ask questions, and the system provides context-aware responses. This script maintains a conversation history, allowing for more relevant and coherent responses in ongoing interactions.

### `cleanup.sh`

A bash script that cleans up the environment by removing downloaded files and directories created during the execution of the project.

### `start.sh`

This script orchestrates the entire workflow. It initiates the cleaning process, runs `webscrape.py` to collect URLs, downloads content using `wget`, and then executes `cleaner.py` and `chunker.py` for processing. The url scraping is done in multi processing. Finally, it runs `main.py` for user interaction.

## Setup and Installation

1. Clone the repository.
2. Install the necessary dependencies using `pip install -r requirements.txt`.
3. Set your OpenAI API key in the `.env` file.
4. Run `start.sh` to begin the process.

## Usage

After setting up, execute `start.sh` with your desired search query. The script manages the entire flow, from downloading articles to processing them and generating AI responses.

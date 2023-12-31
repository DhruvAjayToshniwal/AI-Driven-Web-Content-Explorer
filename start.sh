#!/bin/bash

# Delete the websites directory and train.jsonl file
./cleanup.sh

# Run the Python script to retrieve top URLs
python3 webscrape.py

# Check if the URL file exists and is not empty
if [ ! -s urls.txt ]; then
    echo "No URLs found. Exiting."
    exit 1
fi

# Directory to save the downloaded HTML files
dir="websites"
mkdir -p "$dir"

# Change to the directory
cd "$dir"

# Counter for URLs
count=0

# Read URLs from the file and use wget to download each article
while IFS= read -r url; do
    echo "Downloading $url..."
    wget -nd -A.html "$url" &

    # Increment the counter
    ((count++))

    # For every two URLs, wait for the parallel processes to finish
    if ((count % 2 == 0)); then
        wait
    fi
done < ../urls.txt

# Wait for the last batch of parallel processes to finish
wait

echo "Download completed. Check the '$dir' directory."
cd ..

# Run the Python scripts
python3 cleaner.py
python3 chunker.py
python3 main.py

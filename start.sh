#!/bin/bash

echo "Starting cleanup process..."
./cleanup.sh

echo "Retrieving top URLs..."
python3 webscrape.py

if [ ! -s urls.txt ]; then
    echo "No URLs found. Exiting."
    exit 1
fi

dir="websites"
mkdir -p "$dir"

echo "Changing to directory $dir..."
if cd "$dir"; then
    MAX_PARALLEL=10  # Maximum number of parallel downloads
    count=0

    echo "Starting downloads..."
    while IFS= read -r url; do
        echo "Downloading $url..."
        wget -nd -A.html "$url" &
        ((count++))

        if ((count % MAX_PARALLEL == 0)); then
            wait
        fi
    done < ../urls.txt

    wait
    echo "Download completed. Check the '$dir' directory."
else
    echo "Failed to change directory to $dir. Exiting."
    exit 1
fi

cd ..

echo "Running cleaner script..."
python3 cleaner.py

echo "Running chunker script..."
python3 chunker.py

echo "Executing main script..."
python3 main.py

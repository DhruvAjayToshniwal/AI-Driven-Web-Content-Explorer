echo "Deleting downloaded files and directory..."

dir="websites"
rm -rf "$dir"
rm -f train.jsonl
rm -f urls.txt

echo "Cleanup completed."
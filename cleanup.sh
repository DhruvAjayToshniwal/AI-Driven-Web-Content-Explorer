echo "Deleting downloaded files and directory..."

rm -rf websites
rm -rf cleaned_websites
rm -rf __pycache__
rm -f train.jsonl
rm -f urls.txt
rm -f last_query.txt

echo "Cleanup completed."
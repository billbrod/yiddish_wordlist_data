#!/usr/bin/env bash
set -euo pipefail

Help()
{
   # Display Help
   echo "Add metadata and move file to correct folder. See readme for details."
   echo
   echo "Syntax: add_metadata [-h] inputPath title collection"
   echo
   echo "positional arguments:"
   echo "  inputPath     Path to the json with the wordlist"
   echo "  title         Title of the story (in unicode or YIVO transliteration)"
   echo "  collection    Name of the collection (in unicode or YIVO transliteration)"
   echo
   echo "options:"
   echo "  -h            Print this Help."
   echo
}

while getopts ":h" option; do
   case $option in
      h) # display Help
         Help
         exit 0;;
     \?) # incorrect option
         echo "Error: Invalid option"
         exit 1;;
   esac
done

if [ "$#" -lt 3 ]
then
    Help >&2
    exit 1
fi

transcript=$(./utils/transcribe_yiddish.py "$2")
title_unicode=$(echo "$transcript" | cut -d';' -f2)
if [[ $title_unicode == "unicode" ]]; then
   title=$(echo "$transcript" | cut -d';' -f1)
   title_ascii="$2"
else
   title_ascii=$(echo "$transcript" | cut -d';' -f1)
   title="$2"
fi

transcript=$(./utils/transcribe_yiddish.py "$3")
collection_unicode=$(echo "$transcript" | cut -d';' -f2)
if [[ $collection_unicode == "unicode" ]]; then
   collection=$(echo "$transcript" | cut -d';' -f1)
   collection_ascii="$3"
else
   collection_ascii=$(echo "$transcript" | cut -d';' -f1)
   collection="$3"
fi

outPath="./wordlists/${collection_ascii// /_}/${title_ascii// /_}.json"
echo "Saving new story at ${outPath}"
mkdir -p "./wordlists/${collection_ascii// /_}"

jq --arg title "$title" --arg collection "$collection" '{title: $title, collection: $collection, words: .}' "$1" > "$outPath"
github_url="https://raw.githubusercontent.com/billbrod/yiddish_wordlist_data/main/wordlists/${collection_ascii// /_}/${title_ascii// /_}.json"
jq --arg url "$github_url" --arg title "$title" --arg collection "$collection" '.[$collection][$title] = $url' contents.json | sponge contents.json

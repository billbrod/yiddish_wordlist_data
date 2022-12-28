#!/usr/bin/env bash
set -euo pipefail

Help()
{
   # Display Help
   echo "Use Jochre to run optical character recognition (OCR) on Yiddish text. See readme for details."
   echo
   echo "Syntax: run_jochre [-h] input_path outDir"
   echo
   echo "positional arguments:"
   echo "  inputPath     Path to the pdf to run Jochre on"
   echo "  outDir        Path to the folder to save output in"
   echo
   echo "options:"
   echo "  -h             Print this Help."
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

JOCHRE_BIN=$(ls jochre/bin/jochre-yiddish-*.jar)
JOCHRE_LEXICON=$(ls jochre/resources/jochre-yiddish-lexicon-*.zip)

java -jar -Xmx3G $JOCHRE_BIN command=analyseFile file=$1 outDir=$2 lexicon=$JOCHRE_LEXICON letterModel=jochre/resources/yiddish_letter_model.zip outputFormat=Text

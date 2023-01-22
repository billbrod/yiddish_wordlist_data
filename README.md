# yiddish_wordlist_data
Contains the data for the wordlist

For more sources, see Yiddish Book Center's online [OCR
collection](https://ocr.yiddishbookcenter.org/accounts/login/), and this
[Musterverk
guide](https://www.yiddishbookcenter.org/collections/digital-yiddish-library/Musterverk-fun-der-yidisher-literatur)
is probably a good place to start.

TODO
- write help for jochre
- add script or something to add metadata / run jq on the output of yiddish_wordlist
- add links to related repos etc
- explain contents.json in readme
- add links to original sources for pdfs, potential other sources
- make a zenodo? or osf? project with snipped pdfs
- add text and pdf urls to contents.json ({collection: {title: {json: , txt:, pdf: }}})
- add script to do everything:
    - run_jochre, if necessary
    - yiddish_wordlist.main (make pip-installable)
    - add_metadata.sh
    - update_counts.sh



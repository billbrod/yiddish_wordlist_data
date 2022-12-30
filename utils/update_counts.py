#!/usr/bin/env python3

import json
import argparse
from glob import glob
import pandas as pd


def main(wordlist_path):
    """Update word counts and frequencies.

    Go through all wordlists and update counts/frequencies for each individual
    collection and all stories.

    Parameters
    ----------
    wordlist_path : str
        Root directory of wordlists

    """
    df = []
    jsons = {}
    for js_file in glob(f'{wordlist_path}/*/*json'):
        with open(js_file) as f:
            wordlist = json.load(f)
        if wordlist['collection'] not in jsons.keys():
            jsons[wordlist['collection']] = {wordlist['title']: wordlist}
        else:
            jsons[wordlist['collection']][wordlist['title']] = wordlist
        df.append(pd.DataFrame([{'word': k,
                                 'count (story)': v['count (story)'],
                                 'title': wordlist['title'],
                                 'path': js_file,
                                 'collection': wordlist['collection']}
                                for k, v in wordlist['words'].items()]))
    df = pd.concat(df)

    df['total words'] = df['count (story)'].sum()
    gb = df.groupby('collection')['count (story)'].sum()
    df = df.set_index('collection')
    df['collection total words'] = gb
    df = df.reset_index()

    gb = df.groupby(['collection', 'word'])['count (story)'].sum()
    df = df.set_index(['collection', 'word'])
    df['count (collection)'] = gb
    df = df.reset_index()

    gb = df.groupby(['word'])['count (story)'].sum()
    df = df.set_index(['word'])
    df['count (all)'] = gb
    df = df.reset_index()

    df['frequency (collection)'] = df['count (collection)'] / df['collection total words']
    df['frequency (all)'] = df['count (all)'] / df['total words']

    df = df.set_index(['collection', 'title', 'word'])
    for collection, collection_dict in jsons.items():
        for title, title_dict in collection_dict.items():
            for word, word_dict in title_dict['words'].items():
                df_sel = df.loc[collection, title, word]
                for col in ["count (collection)", "count (all)",
                            "frequency (collection)", "frequency (all)"]:
                    # numpy's int types aren't json-serializable, so we convert
                    # to python's builtin
                    if 'count' in col:
                        word_dict[col] = int(df_sel[col])
                    else:
                        word_dict[col] = float(df_sel[col])
            with open(df_sel['path'], 'w') as f:
                json.dump(title_dict, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Update word counts / frequency for whole corpus.")
    parser.add_argument('wordlist_path', help="Path to the root directory of wordlists")
    args = vars(parser.parse_args())
    main(**args)

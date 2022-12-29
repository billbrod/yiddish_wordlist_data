#!/usr/bin/env python3


from selenium import webdriver
from bs4 import BeautifulSoup
import argparse


def main(words):
    """Transcribe Unicode to YIVO or vice versa.

    If `words` is encodable in ascii, it's all Latin letters, and we thus
    assume it's a YIVO transliteration. If it's not, we assume it's in Hebrew
    letters. We always convert from one to the other.

    This uses the website
    https://www.cs.uky.edu/~raphael/yiddish/makeyiddish.html and uses selenium
    to do so (and thus opens a chrome window).

    Parameters
    ----------
    words : str
        The string to transcribe.

    Returns
    -------
    transcribed : str
        The transcribed string.
    uni_to_yivo : bool
        If True, `words` was unicode (Hebrew letters) and thus `transcribed` is
        the yivo transliteration. If False, `words` was ascii (Latin letters)
        and thus `transcribed` is the Yiddish in Hebrew letters.

    """
    try:
        words.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        uni_to_yivo = True
    else:
        uni_to_yivo = False
    transcript_url = 'https://www.cs.uky.edu/~raphael/yiddish/makeyiddish.html'
    browser = webdriver.Chrome()
    browser.get(transcript_url)
    browser.find_element('name', 'Text').send_keys(words)
    if uni_to_yivo:
        browser.find_element('xpath', '//input[@type="radio" and @name="Input" and @value="UTF-8"]').click()
        browser.find_element('xpath', '//input[@type="radio" and @name="Output" and @value="YIVO"]').click()
    else:
        browser.find_element('xpath', '//input[@type="radio" and @name="Input" and @value="YIVO"]').click()
        browser.find_element('xpath', '//input[@type="radio" and @name="Output" and @value="UTF"]').click()
    browser.find_element('xpath', '//input[@type="submit" and @value="Submit"]').click()
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    if uni_to_yivo:
        words = soup.find('pre').text.strip()
    else:
        words = soup.find('p').text.replace('\n', '').replace('\u200f', '').strip()
    return words, uni_to_yivo


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Transcribe Unicode to YIVO or vice versa.")
    parser.add_argument('words', help="The words to transcribe.")
    args = vars(parser.parse_args())
    if ';' in args['words']:
        raise ValueError("words cannot contain a semicolor (;), since we use this for parsing the output!")
    words, uni_to_yivo = main(**args)
    if uni_to_yivo:
        print(words + ';yivo')
    else:
        print(words + ';unicode')

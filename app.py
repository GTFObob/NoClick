from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from bs4 import BeautifulSoup

import requests.exceptions
import urllib.request

from flask import Flask, request, render_template, abort
from unidecode import unidecode
import json

app = Flask(__name__)

# Route for the summaries; API
@app.route('/summarize', methods = [ "GET" ])
def summarize():

	SENTENCES_COUNT = 5
	LANGUAGE = 'english'

	final = []

	# Checking the integrity of the url query
	url = request.args.get('url')

	
	if(url == None or url == ""):
		return abort(400)

	# Checking the integrity of the num query
	try:
		num = int(request.args.get('num'))
		if(num > 0):
			SENTENCES_COUNT = num
	except (ValueError, TypeError) as e:
		num = None

	# Handles error where url is not a valid url
	try:
		parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
	except (requests.exceptions.MissingSchema, requests.exceptions.HTTPError) as e:
		return "URL is not valid.", 403

	stemmer = Stemmer(LANGUAGE)
	summarizer = Summarizer(stemmer)
	summarizer.stop_words = get_stop_words(LANGUAGE)

	# Take each sentence and append
	for sentence in summarizer(parser.document, SENTENCES_COUNT):
		# unidecode takes unicode characters and converts it into ASCII
		final.append(unidecode(str(sentence)))

	response = urllib.request.urlopen(url)
	html = response.read()

	soup = BeautifulSoup(html)
	title = soup.html.head.title.getText()

	return json.dumps({"title": title, "content":final})

@app.route('/', defaults={'path': ''})
def home(path):
	return render_template("index.html")


@app.route('/<path:path>')
def catch_all(path):
    return abort(404)

if __name__ == "__main__":
	app.run(host='0.0.0.0')

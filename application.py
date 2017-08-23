from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

import requests.exceptions

from flask import Flask, request, render_template
from unidecode import unidecode
import json

application = Flask(__name__)

# Route for the actual summaries
@application.route('/summarize', methods = [ "GET" ])
def summarize():

	SENTENCES_COUNT = 5
	LANGUAGE = 'english'

	final = []

	# Checking the integrity of the url query
	url = request.args.get('url')

	
	if(url == None):
		return render_template("error.html", message = "Invalid Error. Please try again later."), 404

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
		return render_template("error.html", message = url + " is an not a valid URL."), 403


	stemmer = Stemmer(LANGUAGE)
	summarizer = Summarizer(stemmer)
	summarizer.stop_words = get_stop_words(LANGUAGE)

	# Take each sentence and oppend
	for sentence in summarizer(parser.document, SENTENCES_COUNT):
		# unidecode takes unicode characters and converts it into ASCII
		final.append(unidecode(str(sentence)))

	return render_template("index.html", results=final)

@application.route('/', defaults={'path': ''})
@application.route('/<path:path>')
def catch_all(path):
    return "No summary found or invalid link entered.", 403

if __name__ == "__main__":
	application.run(host='0.0.0.0')

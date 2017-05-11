from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from flask import Flask, request
from unidecode import unidecode
import json

application = Flask(__name__)
<<<<<<< HEAD
=======
import nltk
nltk.data.path.append("/usr/local/share/nltk_data")
>>>>>>> 0e69c713c98d7f6b6cfc02c6e35fa0f0ada3950c

# Route for the actual summaries
@application.route('/summarize', methods = [ "GET" ])
def summarize():

	SENTENCES_COUNT = 5
	LANGUAGE = 'english'
	final = []

	# Checking the integrity of the url query
	url = request.args.get('url')


	if(url == None):
		return "Invalid Request", 404

	# Checking the integrity of the num query
	try:
		num = int(request.args.get('num'))
	except ValueError:
		num = None

	if(num != None and num > 0):
		SENTENCES_COUNT = num

	# Parse and Summarize
	parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
	stemmer = Stemmer(LANGUAGE)
	summarizer = Summarizer(stemmer)
	summarizer.stop_words = get_stop_words(LANGUAGE)

	# Take each sentence and oppend
	for sentence in summarizer(parser.document, SENTENCES_COUNT):
		# unidecode takes unicode characters and converts it into ASCII
		final.append(unidecode(str(sentence)))

	return json.dumps(final)

@application.route('/', defaults={'path': ''})
@application.route('/<path:path>')
def catch_all(path):
    return "No summary found or invalid link entered.", 403

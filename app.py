from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from custom_parser import CustomParser as Parser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from flask import Flask, request, render_template, abort
from unidecode import unidecode
import json, requests

app = Flask(__name__)
MIN_SENTENCES_COUNT = 5
MAX_SENTENCES_COUNT = 10
LANGUAGE = 'english'

# Route for the summaries; API
@app.route('/summarize', methods = [ "GET" ])
def summarize():

	final = []

	# Checking the integrity of the url query
	url = request.args.get('url')

	
	if(url == None or url == ""):
		return abort(400)

	# Checking the integrity of the num query
	try:
		num = int(request.args.get('num'))

		num = MIN_SENTENCES_COUNT if num < MIN_SENTENCES_COUNT else num
		num = MAX_SENTENCES_COUNT if num > MAX_SENTENCES_COUNT else num

	except (ValueError, TypeError) as e:
		num = MIN_SENTENCES_COUNT

	# Handles error where url is not a valid url
	try:
		parser = Parser.from_url(url, Tokenizer(LANGUAGE))
	except (requests.exceptions.MissingSchema, requests.exceptions.HTTPError) as e:
		try:
			parser = Parser.from_url("http://" + url, Tokenizer(LANGUAGE))
		except:
			return "URL is not valid.", 403 


	stemmer = Stemmer(LANGUAGE)
	summarizer = Summarizer(stemmer)
	summarizer.stop_words = get_stop_words(LANGUAGE)

	# Take each sentence and append
	for sentence in summarizer(parser.document, num):
		# unidecode takes unicode characters and converts it into ASCII
		final.append(unidecode(str(sentence)))

	return json.dumps({"title": parser.get_title(), "content":final})

@app.route('/', defaults={'path': ''})
def home(path):
	return render_template("index.html")


@app.route('/<path:path>')
def catch_all(path):
    return abort(404)

if __name__ == "__main__":
	app.run(host='0.0.0.0')

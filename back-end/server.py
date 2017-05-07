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

app = Flask(__name__)
SENTENCES_COUNT = 5
LANGUAGE = 'english'


# Route for the actual summaries
@app.route('/summarize', methods = [ "GET" ])
def summarize():
	url = request.args.get('url')

	if(url == None):
		return "Invalid Request", 404

	parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
	stemmer = Stemmer(LANGUAGE)
	summarizer = Summarizer(stemmer)
	summarizer.stop_words = get_stop_words(LANGUAGE)

	final = []

	for sentence in summarizer(parser.document, SENTENCES_COUNT):
		final.append(unidecode(str(sentence).decode('utf-8')))

	return json.dumps(final, encoding='utf-8')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return "No summary found or invalid link entered.", 403
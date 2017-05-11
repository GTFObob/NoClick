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

import sys
print(sys.version_info)

application = Flask(__name__)
import nltk
nltk.data.path.append("/usr/local/share/nltk_data")

# Route for the actual summaries
@application.route('/summarize', methods = [ "GET" ])
def summarize():
        SENTENCES_COUNT = 5
        LANGUAGE = 'english'

        final = []
	url = request.args.get('url')
	num = request.args.get('num')

	if(num != None):
		SENTENCES_COUNT = num

	if(url == None):
		return "Invalid Request", 404

	parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
	stemmer = Stemmer(LANGUAGE)
	summarizer = Summarizer(stemmer)
	summarizer.stop_words = get_stop_words(LANGUAGE)

	for sentence in summarizer(parser.document, SENTENCES_COUNT):
		final.append(unidecode(str(sentence)))

	return json.dumps(final)

@application.route('/', defaults={'path': ''})
@application.route('/<path:path>')
def catch_all(path):
    return "No summary found or invalid link entered.", 403

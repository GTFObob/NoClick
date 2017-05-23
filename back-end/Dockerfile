FROM python:3-onbuild
EXPOSE 5000
RUN python -m nltk.downloader punkt
CMD ["python", "./application.py"]

FROM python:3.9.6-slim-buster
ADD . /twitter-opinion
WORKDIR /twitter-opinion
RUN pip install -r requirements.txt
RUN python3 -m nltk.downloader stopwords
RUN python3 -m nltk.downloader punkt
EXPOSE 5000
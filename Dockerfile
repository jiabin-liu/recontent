FROM python:3.5
MAINTAINER Freija Descamps <freija@gmail.com>
EXPOSE 5000
RUN pip install --upgrade pip
RUN pip install bpython
# pandas takes about 10min to download and install the first time around
RUN pip install pandas
RUN pip install flask && \
    pip install flask-restful && \
    pip install requests
RUN pip install justext
RUN pip install gensim && \
    pip install --upgrade gensim
RUN pip install wget
VOLUME ["/data"]
COPY app/app.py /
COPY app/recommender.py /
COPY tools/make_simple_wiki_corpus.py /
WORKDIR /data
CMD ["sh", "-c", "python /make_simple_wiki_corpus.py && python /app.py"]

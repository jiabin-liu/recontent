FROM python:3.5
MAINTAINER Freija Descamps <freija@gmail.com>
EXPOSE 5000
RUN pip install flask \
                flask-restful \
                requests \
                justext \
                gensim \
                wget
VOLUME ["/data"]
COPY app/ app/
COPY tools/get_simple_wiki_corpus.py /
WORKDIR /data
CMD ["sh", "-c", "pwd && ls -rlth && python /get_simple_wiki_corpus.py && python ../app/app.py"]

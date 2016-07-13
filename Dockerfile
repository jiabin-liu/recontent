FROM python:3.5
MAINTAINER Freija Descamps <freija@gmail.com>
EXPOSE 5000
RUN pip install flask && \
    pip install flask-restful && \
    pip install requests
COPY app/app.py /
COPY app/recommender.py /
CMD ["python", "/app.py"]

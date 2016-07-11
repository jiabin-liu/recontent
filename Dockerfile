FROM python:3.5
MAINTAINER Freija Descamps <freija@gmail.com>
EXPOSE 5000
RUN pip install flask
COPY app.py /
CMD ["python", "/app.py"]

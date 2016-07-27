FROM gliderlabs/alpine:latest
MAINTAINER Freija Descamps <freija@gmail.com>
RUN apk-install curl
CMD ["sh", "-c", "while true; do curl app:5000/api/recommend/v1.0/simple-wiki -X GET -d \"url=http://www.symmetrymagazine.org/article/scientists-salvage-insights-from-lost-satellite\"; sleep 10; done"]

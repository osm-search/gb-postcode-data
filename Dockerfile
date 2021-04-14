FROM postgis/postgis:12-3.1

RUN apt-get update && apt-get -qy install php wget unzip dos2unix

WORKDIR /app

VOLUME /data

COPY convert_codepoint.php /app
COPY convert.sh /app
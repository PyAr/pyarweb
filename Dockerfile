FROM python:3.4-wheezy

VOLUME ["/opt/code"]

RUN apt-get update && apt-get install -y apt-utils cmake gcc make tk-dev libjpeg-dev zlib1g-dev libtiff5-dev libfreetype6-dev liblcms2-dev libwebp-dev libtk-img-doc libopenjpeg-dev

ADD ./scripts/install-openjpeg.sh /tmp/
RUN /tmp/install-openjpeg.sh

COPY ./scripts/webcli.py /webcli

CMD [ "/bin/bash" ]
EXPOSE 8000

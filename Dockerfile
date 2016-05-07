from python:3.4-wheezy
ADD ./requirements.txt /opt/ 
ADD ./scripts/install-openjpeg.sh /opt/
ADD ./scripts/runserver.sh /opt/
RUN chmod +x /opt/runserver.sh && apt-get update && apt-get install -y cmake gcc make tk-dev libjpeg-dev zlib1g-dev libtiff5-dev libfreetype6-dev liblcms2-dev libwebp-dev libtk-img-doc libopenjpeg-dev && /opt/install-openjpeg.sh
RUN pip install -r /opt/requirements.txt
VOLUME ["/opt/code"]
CMD [ "/opt/runserver.sh" ]
EXPOSE 8000

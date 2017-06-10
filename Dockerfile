FROM python:2.7

MAINTAINER Fco. Javier Picado Ladrón de guevara millaguie @github


COPY . /server
WORKDIR /server
RUN pip install -r requirements.txt
RUN git clone https://github.com/millaguie/Vernam.git && cd Vernam && pip install -r requirements.txt && cd .. && mv Vernam /tmp/ && mv /tmp/Vernam/vernam  /server/ && rm -rf /tmp/Vernam
EXPOSE 8180
VOLUME /server/passwords.yaml
VOLUME /server/keyfile
VOLUME /server/keyfile.yaml
ENTRYPOINT ["./server.py"]

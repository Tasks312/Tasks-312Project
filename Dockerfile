FROM python:3.8
ENV HOME /root
WORKDIR /root

RUN apt-get update --fix-missing

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

# Download dependancies
RUN apt install -y python3-flask

COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 8080
CMD /wait && flask --app App run --host=0.0.0.0 -p 8080
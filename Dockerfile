FROM ubuntu

WORKDIR /app

RUN apt-get update
RUN apt-get install python3 -y

COPY mainfwftocsv.py filespecclass.py makefwf.py ./

COPY ./input/spec.json ./input/

CMD ["bash"]


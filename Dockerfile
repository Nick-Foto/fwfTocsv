FROM ubuntu

#FROM alpine

WORKDIR /app

RUN apt-get update
RUN apt-get install python3.6.9 -y

COPY mainfwftocsv.py filespecclass.py makefwf.py ./

COPY ./input/spec.json ./input/



#CMD ["python", "mainfwftocsv.py"]
#ENTRYPOINT ["python3", "mainfwftocsv.py"]
CMD ["bash"]


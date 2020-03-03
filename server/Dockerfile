FROM python:3.6

EXPOSE 5000

WORKDIR /server

COPY requirements.txt /server
RUN pip install -r requirements.txt

COPY server.py /server
CMD python server.py

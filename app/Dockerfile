FROM python:3.10.5

RUN mkdir /workspace
WORKDIR /workspace
ADD requirements.txt /workspace/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /workspace/
CMD python3 manage.py runserver 0.0.0.0:8000
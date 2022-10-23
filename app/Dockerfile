FROM python:3.10.5

# RUN mkdir /workspace
# WORKDIR /workspace
# ADD requirements.txt /workspace/
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
# ADD . /workspace/

ADD requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . ./
RUN mkdir -p /var/run/gunicorn
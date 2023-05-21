FROM python

RUN useradd -ms /bin/bash aviv

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

RUN curl -fsSLO 
https://get.docker.com/builds/Linux/x86_64/docker-17.04.0-ce.tgz \
  && tar xzvf docker-17.04.0-ce.tgz \
  && mv docker/docker /usr/local/bin \
  && rm -r docker docker-17.04.0-ce.tgz

USER aviv

WORKDIR /home/aviv/app

COPY . .

CMD ["gunicorn","-w", "3" ,"--bind", "0.0.0.0:5000", "wsgi:app"]


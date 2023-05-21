FROM python

RUN useradd -ms /bin/bash aviv

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

USER aviv

WORKDIR /home/aviv/app

COPY . .

CMD ["gunicorn","-w", "3" ,"--bind", "0.0.0.0:5000", "wsgi:app"]


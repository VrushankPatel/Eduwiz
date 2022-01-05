FROM python

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

EXPOSE $PORT

#RUN python3 manage.py makemigrations
#RUN python3 manage.py migrate

CMD python3 manage.py runserver 0.0.0.0:$PORT
FROM python:3.9.5

COPY requirements.txt /tmp/
RUN pip install --upgrade pip && pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /home/didar/didar-backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .
COPY .env .env

RUN python manage.py collectstatic --noinput
#RUN python manage.py migrate

#CMD ["gunicorn", "--bind", ":8000", "didar.wsgi:application"]

COPY start.sh /start.sh

RUN chmod +x /start.sh

CMD ["/start.sh"]

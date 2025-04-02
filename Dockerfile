FROM python:3.9.5

COPY requirements.txt /tmp/
RUN pip install --upgrade pip && pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /home/didar/didar-backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG SECRET_KEY
# a secret key just for development build
ENV SECRET_KEY="anunsecuresecrectkey"

COPY . .

RUN python manage.py collectstatic --noinput

COPY start.sh /start.sh

RUN chmod +x /start.sh

CMD ["/start.sh"]

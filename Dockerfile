from python

LABEL org.opencontainers.image.authors="minkhantzaw.personal@gmail.com"

COPY . /app/

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD [ "python3", "main.py"]
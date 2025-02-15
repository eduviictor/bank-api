FROM python:3.12

WORKDIR /home/app

COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod 755 /usr/local/bin/entrypoint.sh && ln -s /usr/local/bin/entrypoint.sh && pip install --upgrade pip && pip install poetry==1.8

EXPOSE 80

ENTRYPOINT [ "bash" ]
CMD [ "entrypoint.sh" ]

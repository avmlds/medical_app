FROM python:3.9-buster
WORKDIR /app/
COPY ./app /app
RUN pip3 install cython uvicorn
RUN pip3 install -r requirements.txt
ENV PYTHONPATH=/app
RUN ["chmod", "+x", "prestart.sh"]
CMD ["/bin/sh", "prestart.sh"]
FROM python:3.9-buster
RUN pip3 install cython
RUN mkdir /app
WORKDIR /app/
COPY ./ /app/
RUN pip install -r requirements.txt
CMD ["python3.9", "main.py"]
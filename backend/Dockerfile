FROM python:3.9-buster
RUN pip3 install cython uvicorn
RUN mkdir /app
WORKDIR /app/
COPY ./ /app/
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
FROM python:3.9.5-slim
WORKDIR /src
COPY ./src/requirements.txt .
COPY ./src/app.py .
RUN pip3 install -r requirements.txt
EXPOSE 8050
CMD python3 app.py
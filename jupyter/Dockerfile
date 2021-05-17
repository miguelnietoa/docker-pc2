FROM python:3.9.5-slim
WORKDIR /notebooks
COPY ./notebooks/requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8888
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
FROM python:3.10
COPY . .
WORKDIR . 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
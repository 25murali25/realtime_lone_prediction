FROM python:3.10-slim

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

EXPOSE 8001

CMD ["uvicorn", "app_back:app", "--host", "0.0.0.0", "--port", "8001"]
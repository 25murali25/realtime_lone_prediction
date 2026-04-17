FROM python:3.10-slim
WORKDIR /app_back.py
COPY app_back.py/ .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app_back:app", "--host", "0.0.0.0", "--port", "8000"]


FROM python:3.11-slim
WORKDIR /app
COPY ../../requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY services/streamlit_app/app /app
EXPOSE 8501
CMD ["streamlit", "run", "logisense_app.py", "--server.port=8501", "--server.address=0.0.0.0"]

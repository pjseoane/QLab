FROM python:3.13-slim
LABEL authors="pauli"

WORKDIR /app

COPY requirements.txt .
#COPY external_libs/pjs_qlab-0.2.1-py3-none-any.whl .
#RUN pip install pjs_qlab-0.2.1-py3-none-any.whl
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
FROM python:3.12-slim
LABEL authors="pauli"

WORKDIR /app

COPY QLab/requirements.txt ./requirements.txt
COPY pjs_qlab /pjs_qlab
RUN python -m pip install --no-cache-dir --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY QLab/ .

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

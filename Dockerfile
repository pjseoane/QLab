FROM python:3.13-slim
LABEL authors="pauli"

WORKDIR /app

COPY requirements.txt .
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/pjseoane/pjs_qlab.git


EXPOSE 8501

CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
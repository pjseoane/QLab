#to build and run from container
docker build -t streamlit_app .
docker run -p 8501:8501 streamlit_app

#to run alone
streamlit run app/main.py
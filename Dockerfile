FROM python:3.7

RUN mkdir -p /usr/scr/app/
WORKDIR /usr/scr/app/
COPY requirements.txt ./requirements.txt
RUN xargs -L 1 pip install < requirements.txt
EXPOSE 8080
COPY . /usr/scr/app/
CMD ["streamlit", "run", "app.py"]
#CMD streamlit run --server.port 8080 --server.enableCORS false app.py

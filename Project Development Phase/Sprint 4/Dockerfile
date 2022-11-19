FROM python:3.10.4
WORKDIR /app
ADD . .
RUN pip install -r requirements.txt
CMD ["python","./app.py"]
EXPOSE 5000
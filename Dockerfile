FROM python:3.8.10
WORKDIR /code
RUN apt-get update && apt install build-essential --fix-missing -y
RUN apt-get install ffmpeg -y
COPY ./requirements.txt /code/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
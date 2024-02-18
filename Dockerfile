# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR /flask-blog

RUN python3.11 -m venv .venv

# activate the vitual environment
RUN . .venv/bin/activate

# copy the requirements file and install the dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy the code to the container directory defined above
COPY . .

CMD python -m flask --app blog run --host 0.0.0.0

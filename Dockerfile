FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# Expose the port that the application listens on.
EXPOSE 8000

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]

# use the official Python base image
FROM python:3.9

# set the working directory... thank you Jesus!
WORKDIR /code

# copy requirements.txt
COPY ./requirements.txt /code/requirements.txt

# tell pip not to save the packages locally
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy the hapy-land source to app directory
COPY ./hapy-land /code/app

# run the uvicorn command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--restart"]



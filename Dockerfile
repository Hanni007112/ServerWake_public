FROM python:3.8.3-slim

WORKDIR /usr/src/app

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

#install dependencies
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
                        
COPY ./webserver /usr/src/app/
RUN pip install -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate



EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
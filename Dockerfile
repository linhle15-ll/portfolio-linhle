FROM python:3.9-slim-buster

WORKDIR /myportfolio

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]

EXPOSE 5000

# docker build -t myportfolio_iamge .
# docker run --name myportfolio --env TESTING=true --publish "5000:5000" --detach myportfolio_image 



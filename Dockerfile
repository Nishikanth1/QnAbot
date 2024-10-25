FROM python:3.11-slim-bookworm
EXPOSE 5000
WORKDIR /qnabot
COPY ./setup/requirements.txt /qnabot/setup/requirements.txt
RUN pip install -r /qnabot/setup/requirements.txt

COPY . /qnabot
CMD [ "python3.11", "-m" , "flask", "run", "--host=0.0.0.0"]
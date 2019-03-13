FROM python:3.5
WORKDIR /haca_bot
ENV TZ 'Asia/Tehran'
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./ /haca_bot
CMD ["python -m", "english_class/bot/controllers/sender"]
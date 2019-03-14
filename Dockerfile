FROM python:3.5
WORKDIR /english
ENV TZ 'Asia/Tehran'
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./ ./
RUN pip install -e .
CMD ["python", "english_class/bot/controllers/sender.py"]
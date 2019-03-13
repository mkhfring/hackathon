import os


class DbConfig:
    database_url = "sqlite:///{}".format("practice_db")


class BotConfig:
    token = os.environ.get('BOT_TOKEN', '1254471079:966a4cd79b0c28fca23e9d37fb1473243a3b9468')
    base_url = os.environ.get('BASE_URL', 'https://tapi.bale.ai/')
    base_file_url = os.environ.get('BASE_FILE_URL', 'https://tapi.bale.ai/file/"')


class InvoiceConfig:
    provider_token = os.environ.get('PROVIDER_TOKEN', '6037111122223333')
    amount = os.environ.get('AMOUNT', 1000)

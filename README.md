# ios-push-notification
Apps to send notifications for macOS if the price of Bitcoin is higher than previously set.

1. Create .env file: touch .env
2. Add key=value: BASE_URL=https://coinmarketcap.com/currencies/bitcoin/
3. Uplaoding environment: export $(cat .env | xargs)
4. Uploading packages: python -m pip install -r requirements.txt
5. Start app: python main.py
6. Specify a target price, for example, 10.00

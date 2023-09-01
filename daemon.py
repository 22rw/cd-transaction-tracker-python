import configparser
from datetime import date, datetime, timedelta
from comdirect_api.comdirect_client import ComdirectClient

if __name__ == '__main__':
    config = configparser.ConfigParser()

    config.read('creds.ini')

    if 'creds' not in config:
        print('Error: please supply your credentials, then restart!')

    client_id = config['creds']['clientId']
    client_secret = config['creds']['clientSecret']

    username = input('Please input your comdirect username \n')
    pin = input('Please input your pin \n')

    client = ComdirectClient(client_id, client_secret)

    input('Running initial flow, do not forget to activate the TAN in your photoTAN App \nPress ENTER to continue...')

    client.fetch_tan(username, pin)

    input('Press ENTER after completing the TAN challenge...')

    client.activate_session()

    transactions = client.get_account_transactions(
        '07782CC76AF84928A0D1271993A8C55F',
        False,
        'BOTH',
        20,
        0,
        str((datetime.today() - timedelta(days=2)).date()),
        str(date.today())
    )

    for transaction in transactions['values']: 
        print(
            'remitter: '
            + str(transaction['remitter']) 
            + ' | debtor: ' 
            + str(transaction['debtor'])
            + ' | creditor: '
            + str(transaction['creditor'])
            + ' | amount: '
            + str(transaction['amount'])
        )

    input('Press ENTER to exit...')

    



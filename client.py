import configparser
from datetime import date, datetime, timedelta
from comdirect_api.comdirect_client import ComdirectClient

def pollTransactions(client: ComdirectClient, daydelta: int = 1) -> list:
    transactions = client.get_account_transactions(
        '07782CC76AF84928A0D1271993A8C55F',
        False,
        'BOTH',
        20,
        0,
        str((datetime.today() - timedelta(days=daydelta)).date()),
        str(date.today())
    )

    transaction_list = []

    for transaction in transactions['values']:
        desc = ''
        if 'remitter' in transaction and transaction['remitter'] != None or '':
            desc = ' remitter: ' + str(transaction['remitter'])
        elif 'debtor' in transaction and transaction['debtor'] != None or '':
            desc = ' debtor: ' + str(transaction['debtor'])
        elif 'creditor' in transaction and transaction['creditor'] != None or '':
            desc = ' creditor: ' + str(transaction['creditor'])
        
        transaction_list.append({
            'Description': desc,
            'Type': transaction['transactionType'],
            'Date': transaction['bookingDate'],
            'Amount': str(transaction['amount']['value']) + ' ' + str(transaction['amount']['unit']) ,
        })

    return transaction_list



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

    for transaction in pollTransactions(client, 40):
        print(transaction)

    input('Press ENTER to exit...')

    



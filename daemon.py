import configparser
from comdirect_api.comdirect_client import ComdirectClient

if __name__ == '__main__':
    config = configparser.ConfigParser()

    with open('creds.ini') as credfile:
        config.read(credfile)
        client_id = config['clientId']
        client_secret = config['clientSecret']

    username = input('Please input your comdirect username.')
    pin = input('Please input your pin')

    client = ComdirectClient(client_id, client_secret)

    input('Running initial flow, do not forget to activate the TAN in your photoTAN App')

    client.fetch_tan(username, pin)

    client.activate_session()

    balances = client.get_all_balances()
    print(balances['values'])

    



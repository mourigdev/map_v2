from requests import get

ip = get('https://api.seeip.org').text
print('My public IP address is: {}'.format(ip))
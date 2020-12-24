import client

client = client.Client()
client.link()
info = {'mode': 'sendMajor', 'Major': 'math'}

client.send_info(info)

mode, message = client.receive_info()

print(mode)
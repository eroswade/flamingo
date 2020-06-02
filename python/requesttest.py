import requests

sess = requests.Session()


url = 'http://127.0.0.1/test.html'

f = {
        "id": 1,
        "name": 'eros',
        "type": 'test'
    }

result = sess.get(url, data = f)
print(result)
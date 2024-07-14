import requests

url = 'http://127.0.0.1:5000/api/search'
file_path = 'path_to_your_image.jpg'

with open(file_path, 'rb') as f:
    files = {'file': f}
    response = requests.post(url, files=files)

if response.status_code == 200:
    data = response.json()
    print('Query Image:', data['query_path'])
    for score, path in data['scores']:
        print(f'Score: {score}, Path: {path}')
else:
    print('Error:', response.json()['error'])

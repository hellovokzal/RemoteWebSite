from os import system
try:
    from flask import Flask, send_file, request
except ModuleNotFoundError:
    system("pip install flask")
    from flask import Flask, send_file, request
try:
  import requests
except:
  system("pip install requests")
  import requests
try:
  from io import BytesIO
except:
  system("pip install io")
  from io import BytesIO
try:
  from time import sleep
except:
  system("pip install time")
  from time import sleep
try:
  from threading import Thread
except:
  system("pip install threading")
  from threading import Thread

id = 0
link = ""
link1 = ""
url = input("Введите ссылку вашего сайта: ")

def timer():
  global link, link1
  while True:
    sleep(0.01)
    with open("link.txt", "r") as f:
      link = f.read() 
    link1 = f"{link}/"

start = Thread(target=timer)
start.start()

app = Flask(__name__)

@app.route("/")
def index():
    global link, link1, id, url
    url = link
    response = requests.get(url)
    response = response.text.replace(link1, url)
    response = response.replace(link1, url)
    id = id + 1
    return f"<title>ID Load: {id}</title>\n{response}"

@app.route("/<path:file1>")
def echo_file(file1):
    global link1, id, url
    id = id + 1
    url = f"{link1}{file1}"
    response = requests.get(url)
    file_to_send = BytesIO(response.content.replace(link1.encode(), url.encode()))
    return send_file(file_to_send, as_attachment=True, download_name=file1)

@app.route("/send", methods=["POST"])

def echo_text():
  data = request.json
  with open("link.txt", "w") as f1:
      f1.write(str(data))
  return "OK"
      
if __name__ == '__main__':
    app.run(host="0.0.0.0")

import requests

url_path = "http://crudsystem0124.pythonanywhere.com"


def getApplicant(data):

	r = requests.get(f'{url_path}/getApplicant', params=data)
	return r.json()


def getApplicantDetail(appId):

	r = requests.get(f'{url_path}/getApplicantdetail', params={'id': appId})
	text = "Salom aleykum"
	text = f""" 
👤 Имя и Фамилия: {r.json()['first_name']} {r.json()['last_name']}

📱 Номер телефона: {r.json()['phone_number']}

🛠Специальность: {r.json()['skills']}

📆 График работы: {r.json()['schedule']}

🔧 Опыт: {r.json()['experence']}

💸 Цена: {r.json()['price']}
	"""
	return text

def createapplicant(data):




	r = requests.post(f'{url_path}/createApplicant', json=data)
	print(r.json())
	return 1


def fedbackView(data):

	
	r = requests.post('http://crudsystem0124.pythonanywhere.com/fedbackView', json=data)
	print(r.json())
	return r.json()


def addServicerequest(text):

	url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id=1552963443&text={text}"
	r = requests.post(url, json={})
	return 1


def send_offer_text(text):

	url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id=1552963443&text={text}"
	r = requests.post(url, json={})
	return 1


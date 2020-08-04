from flask import Flask,request

import requests
from  requests.auth import HTTPBasicAuth
import json


app=Flask(__name__)



#mpesa details
consumer_key='Gsg8RfQviO23dWHD5GG0bKhqKuQRHK7b'
consumer_secret='ungEvOQlvrycN9FM'
base_url='http://192.168.43.37:5000/'

@app.route('/')
def home():
	return "Hello World"

@app.route('/access_token')
def token():
	data=ac_token()
	return data

def ac_token():
	mpesa_auth_url="https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
	#sending a request to Daraja requires that you send an authentication header
	data=(requests.get(mpesa_auth_url,auth=HTTPBasicAuth(consumer_key,consumer_secret))).json()

	return data['access_token']

@app.route('/register_urls')
def register():
	mpesa_endpoint="https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
	headers={"Authorization":"Bearer %s" % ac_token()}
	req_body={
		"ShortCode":"600579",
		"ResponseType":"Completed",
		"ConfirmationURL":base_url+'/c2b/confirm',
		"ValidationURL":base_url+'/c2b/validation'
	}

	response_data=requests.post(
		mpesa_endpoint,
		json = req_body,
		headers=headers
	)

	return response_data.json()


@app.route('/c2b/confirm')
def confirm():
	#get data
	 data=request.get_json()
	 #write in file
	 file=open('confirm.json','a')
	 file.write(data)
	 file.close()

@app.route('/c2b/validation')
def validation():
	#get data
	 data=request.get_json()
	 #write in file
	 file=open('validate.json','a')
	 file.write(data)
	 file.close()




if __name__=='__main__':
	#app.run(debug=True)
	app.run(host='192.168.43.37')

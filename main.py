from flask import Flask, flash, render_template, request
from flask_mqtt import Mqtt

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 1

mqtt = Mqtt(app)
light1st = "0"
light2st = "0"
temp = None

@mqtt.on_connect()
def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("connected to broker")
		mqtt.subscribe("light1st")
		mqtt.subscribe("light2st")
		mqtt.subscribe("tempst")

@mqtt.on_message()
def on_message(client, userdata, message):
	if message.topic == "light1st":
		print(message.topic)
		print(str(message.payload))
		if str(message.payload) == "b'0'":
			global light1st
			light1st = "0"
		elif str(message.payload) == "b'1'":
			global light1st
			light1st = "1"
	elif message.topic == "light2st":
		print(message.topic)
		print(str(message.payload))
		if str(message.payload) == "b'0'":
			global light2st
			light2st = "0"		
		elif str(message.payload) == "b'1'":
			global light2st
			light2st = "1"
	elif message.topic == "tempst":
		global temp
		temp = str(message.payload)[1:]

# @app.route('/, ')
@app.route('/')
def helo():
	return render_template('index.html', temp=temp, light1st=light1st, light2st=light2st)


@app.route('/light1cmd', methods=['POST'])
def light1cmd():
	if request.method == "POST":
		msg = request.form.get("button")
		mqtt.publish("light1", msg)
		return render_template('success.html')

@app.route('/light2cmd', methods=['POST'])
def light2cmd():
	if request.method == "POST":
		msg = request.form.get("button")
		mqtt.publish("light2", msg)
		return render_template('success.html')

if __name__ == '__main__':
	app.run(host="localhost", port='1999')
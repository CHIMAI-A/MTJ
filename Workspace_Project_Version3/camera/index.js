const mqtt = require('mqtt');
const mongoose = require('mongoose');
const shortid = require('shortid');

const Events = require('./eventsModel');
const client = mqtt.connect('mqtt://broker.hivemq.com:1883');

const topic = "esp32/cam/person/dev_1";

//MongoDB Connection Success
mongoose.connection.on('connected', async() => {
    console.log('MongoDB connected');
})

//MongoDB Connection Fail
mongoose.connection.on('error', async(err) => {
    console.log('Error connecting MongoDB', err);
})
client.on('connect', async () => {
    console.log('MQTT Connected');

    client.subscribe(topic);
});

client.on('message', async (topic, message) => {
    console.log('MQTT Received Topic: ', topic, ', Message: ', message);
    
})

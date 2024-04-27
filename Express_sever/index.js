import express from "express";
import { connect } from "mqtt";
import http from "http";
import { Server } from "socket.io";
import cors from "cors";
import mongoose from "mongoose";
import bodyParser from "body-parser";
import { ZoneA, ZoneB, LightZoneA, LightZoneB } from "./db/models.js";

let currentStateZoneA = 0; // current state of pin
let previousStateZoneA = 0; // previous state of pin

let currentStateZoneB = 0; // current state of pin
let previousStateZoneB = 0; // previous state of pin

let currentStateLightZoneA = 0; // current state of pin
let previousStateLightZoneA = 0; // previous state of pin

let currentStateLightZoneB = 0; // current state of pin
let previousStateLightZoneB = 0; // previous state of pin

const prisma = new PrismaClient();
const app = express();
const server = http.createServer(app);

app.use(bodyParser.json());

mongoose.connect("mongodb://localhost:27017/Park_Light", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});


mqttClient.on("connect", function () {
  // Once connected, subscribe to a topic

  mqttClient.subscribe("esp32_S3_Box_ZoneOne");
  mqttClient.subscribe("esp32_S3_Box_ZoneOne/cam/detect");
  mqttClient.subscribe("esp32_dev_ZoneOne");
  mqttClient.subscribe("esp32_dev_ZoneOne/light/brightness");

  mqttClient.subscribe("esp32_S3_Box_ZoneTwo");
  mqttClient.subscribe("esp32_S3_Box_ZoneTwo/cam/detect");
  mqttClient.subscribe("esp32_dev_ZoneTwo");
  mqttClient.subscribe("esp32_dev_ZoneTwo/light/brightness");
});



const updateOrCreateZoneA = (personCount) =>
  updateOrCreateZone(ZoneA, personCount);
const updateOrCreateZoneB = (personCount) =>
  updateOrCreateZone(ZoneB, personCount);

const updateOrCreateLightZoneA = (unit) =>
  updateOrCreateLightZone(LightZoneA, unit);
const updateOrCreateLightZoneB = (unit) =>
  updateOrCreateLightZone(LightZoneB, unit);


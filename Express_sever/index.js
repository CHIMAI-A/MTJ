import express from "express";
import { connect } from "mqtt";
import http from "http";
import { Server } from "socket.io";
import cors from "cors";
//import { PrismaClient } from "@prisma/client";
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

//Setup section
//const prisma = new PrismaClient();
const app = express();
const server = http.createServer(app);

app.use(bodyParser.json());

mongoose.connect("mongodb://localhost:27017/Park_Light", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

//websockeet sever setup
const io = new Server(server, {
  cors: {
    origin: "*", // This should match the client's origin
    methods: ["GET", "POST"],
    allowedHeaders: ["my-custom-header"],
    credentials: true,
  },
});
const port = 3000;
app.use(cors());
//Connect to an MQTT broker
const mqttClient = connect("mqtt://172.20.10.4:1883"); // 127.0.0.1

//MQTT connection
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

// MQTT message event handler (Like callback function) ESP 32 and node sever (backend)
mqttClient.on("message", async (topic, message) => {
  //******************************Zone A **************************************
  if (topic === "esp32_S3_Box_ZoneOne") {
    console.log(message.toString());
  }
  if (topic === "esp32_S3_Box_ZoneOne/cam/detect") {
    previousStateZoneA = currentStateZoneA;
    currentStateZoneA = Number(message.toString());
    if (previousStateZoneA !== currentStateZoneA) {
      io.sockets.emit("esp32_S3_Box_ZoneOne/cam/detect", message.toString());
      const personCount = Number(message.toString());
      await updateOrCreateZoneA(personCount);
      // console.log(message.toString());
    }
  }
  if (topic === "esp32_dev_ZoneOne") {
    console.log(message.toString());
  }
  if (topic === "esp32_dev_ZoneOne/light/brightness") {
    previousStateLightZoneA = currentStateLightZoneA;
    currentStateLightZoneA = Number(message.toString());
    if (previousStateLightZoneA !== currentStateLightZoneA) {
      io.sockets.emit("esp32_dev_ZoneOne/light/brightness", message.toString()); // topic message send to frontend
      const unit = Number(message.toString());
      await updateOrCreateLightZoneA(unit);
      // console.log(message.toString());
    }
  }

  // ***************************** Zone B **************************************
  if (topic === "esp32_S3_Box_ZoneTwo") {
    console.log(message.toString());
  }
  if (topic === "esp32_S3_Box_ZoneTwo/cam/detect") {
    previousStateZoneB = currentStateZoneB;
    currentStateZoneB = Number(message.toString());
    if (previousStateZoneB !== currentStateZoneB) {
      io.sockets.emit("esp32_S3_Box_ZoneTwo/cam/detect", message.toString());
      const personCount = Number(message.toString());
      await updateOrCreateZoneB(personCount); //to save data in database
      // console.log(message.toString());
    }
  }
  if (topic === "esp32_dev_ZoneTwo") {
    console.log(message.toString());
  }
  if (topic === "esp32_dev_ZoneTwo/light/brightness") {
    previousStateLightZoneB = currentStateLightZoneB;
    currentStateLightZoneB = Number(message.toString());
    if (previousStateLightZoneB !== currentStateLightZoneB) {
      io.sockets.emit("esp32_dev_ZoneTwo/light/brightness", message.toString());
      const unit = Number(message.toString());
      await updateOrCreateLightZoneB(unit);
      // console.log(message.toString());
    }
  }

  // ******************************* All Zone ***********************************
});
// websocket section frontend nodesever(backend)
io.on("connection", (socket) => {
  console.log("New client connected!");

  socket.on("zoneOne/emergency_light/control", (msg) => {
    // '.on' is like listen with this topic ' from front end
    console.log(`Control message received : ${msg}`); // to test dataflow
    mqttClient.publish("zoneOne/emergency_light/control", msg); // to ESP 32

    io.sockets.emit("zoneOne/emergency_light/control", msg); // self
  });

  socket.on("zoneTwo/emergency_light/control", (msg) => {
    console.log(`Control message received : ${msg}`); // to test dataflow
    mqttClient.publish("zoneTwo/emergency_light/control", msg);

    io.sockets.emit("zoneTwo/emergency_light/control", msg);
  });

  socket.on("disconnect", () => {
    console.log("Client disconnected");
  });
});

// ************************** http section **************************  ( get old data within one)

app.get("/zoneA/totalVisitors", async (req, res) => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const tomorrow = new Date(today.getTime() + 24 * 60 * 60 * 1000);

  const zoneA = await ZoneA.findOne({
    updatedAt: { $gte: today, $lt: tomorrow },
  });

  if (zoneA) {
    res.send({ total: zoneA.count });
  } else {
    res.send({ total: 0 });
  }
});

app.get("/zoneB/totalVisitors", async (req, res) => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const tomorrow = new Date(today.getTime() + 24 * 60 * 60 * 1000);

  const zoneB = await ZoneB.findOne({
    updatedAt: { $gte: today, $lt: tomorrow },
  });

  if (zoneB) {
    res.send({ total: zoneB.count });
  } else {
    res.send({ total: 0 });
  }
});
app.get("/allZone/totalVisitors", async (req, res) => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const tomorrow = new Date(today.getTime() + 24 * 60 * 60 * 1000);

  try {
    const zoneA = await ZoneA.findOne({
      updatedAt: { $gte: today, $lt: tomorrow },
    });
    const zoneB = await ZoneB.findOne({
      updatedAt: { $gte: today, $lt: tomorrow },
    });

    // Calculate total visitors
    const totalVisitors = (zoneA ? zoneA.count : 0) + (zoneB ? zoneB.count : 0);

    res.send({ total: totalVisitors });
  } catch (error) {
    console.error("Error fetching visitor data:", error);
    res.status(500).send({ error: "Internal Server Error" });
  }
});
app.get("/chart/data", async (req, res) => {
  try {
    // Fetch all data from ZoneA and ZoneB collections
    const dataA = await ZoneA.find({}, "updatedAt count -_id"); // Select only updatedAt and count
    const dataB = await ZoneB.find({}, "updatedAt count -_id");

    let combinedData = {};

    // Combine data from ZoneA
    dataA.forEach((item) => {
      const date = item.updatedAt.toISOString().split("T")[0]; // Formats date to 'YYYY-MM-DD'
      if (!combinedData[date]) {
        combinedData[date] = { zoneA: 0, zoneB: 0 };
      }
      combinedData[date].zoneA += item.count;
    });

    // Combine data from ZoneB
    dataB.forEach((item) => {
      const date = item.updatedAt.toISOString().split("T")[0];
      if (!combinedData[date]) {
        combinedData[date] = { zoneA: 0, zoneB: 0 };
      }
      combinedData[date].zoneB += item.count;
    });

    let formattedData = [];

    // Prepare data for the chart
    Object.keys(combinedData).forEach((date) => {
      formattedData.push({
        date: date,
        type: "ZoneA",
        value: combinedData[date].zoneA,
      });
      formattedData.push({
        date: date,
        type: "ZoneB",
        value: combinedData[date].zoneB,
      });
      formattedData.push({
        date: date,
        type: "AllZone",
        value: combinedData[date].zoneA + combinedData[date].zoneB,
      });
    });

    // Sort data by date
    formattedData.sort((a, b) =>
      a.date > b.date ? 1 : b.date > a.date ? -1 : 0
    );

    res.send(formattedData);
  } catch (error) {
    console.error("Error fetching chart data:", error);
    res.status(500).send({ error: "Internal Server Error" });
  }
});

const updateOrCreateZone = async (model, personCount) => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const tomorrow = new Date(today.getTime() + 24 * 60 * 60 * 1000);

  const zone = await model.findOne({
    updatedAt: { $gte: today, $lt: tomorrow },
  });

  if (zone) {
    zone.count += personCount;
    await zone.save();
  } else {
    const newZone = new model({ count: personCount });
    await newZone.save();
  }
};

const updateOrCreateLightZone = async (model, unit) => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const tomorrow = new Date(today.getTime() + 24 * 60 * 60 * 1000);

  const zone = await model.findOne({
    updatedAt: { $gte: today, $lt: tomorrow },
  });

  if (zone) {
    zone.unit += unit;
    await zone.save();
  } else {
    const newZone = new model({ unit: unit });
    await newZone.save();
  }
};

const updateOrCreateZoneA = (personCount) =>
  updateOrCreateZone(ZoneA, personCount);
const updateOrCreateZoneB = (personCount) =>
  updateOrCreateZone(ZoneB, personCount);

const updateOrCreateLightZoneA = (unit) =>
  updateOrCreateLightZone(LightZoneA, unit);
const updateOrCreateLightZoneB = (unit) =>
  updateOrCreateLightZone(LightZoneB, unit);

server.listen(port, "172.20.10.4", () => {
  console.log(`Example app listening at port:${port}`);
});

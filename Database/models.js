// models.js
import { Schema, model } from "mongoose";

const zoneASchema = new Schema(
  {
    count: {
      type: Number,
      default: 0,
    },
    updatedAt: {
      type: Date,
      default: Date.now,
    },
  },
  { timestamps: { createdAt: false, updatedAt: true } }
);

const zoneBSchema = new Schema(
  {
    count: {
      type: Number,
      default: 0,
    },
    updatedAt: {
      type: Date,
      default: Date.now,
    },
  },
  { timestamps: { createdAt: false, updatedAt: true } }
);

const lightZoneASchema = new Schema(
  {
    unit: {
      type: Number,
      default: 0,
    },
    updatedAt: {
      type: Date,
      default: Date.now,
    },
  },
  { timestamps: { createdAt: false, updatedAt: true } }
);

const lightZoneBSchema = new Schema(
  {
    unit: {
      type: Number,
      default: 0,
    },
    updatedAt: {
      type: Date,
      default: Date.now,
    },
  },
  { timestamps: { createdAt: false, updatedAt: true } }
);

export const ZoneA = model("ZoneA", zoneASchema);
export const ZoneB = model("ZoneB", zoneBSchema);
export const LightZoneA = model("LightZoneA", lightZoneASchema);
export const LightZoneB = model("LightZoneB", lightZoneBSchema);

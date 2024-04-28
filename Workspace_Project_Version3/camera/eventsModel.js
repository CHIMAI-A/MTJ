const mongoose = require('mongoose');
const moment = require('moment');

const Schema = mongoose.Schema;

const EventsSchema = new Schema({
    status_id: {
        type: String,
        required:true
    },
    timestamp: {
        type: Number,
        required:false
    },
    detected: {
        type: Boolean,
        required:true
    },
    centroid_x: {
        type: Number,
        required:true
    },
    centroid_y: {
        type: Number,
        required:true
    },
    total: {
        type: Number,
        required:true
    }
})
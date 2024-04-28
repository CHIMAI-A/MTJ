/* Edge Impulse Arduino examples
 * Copyright (c) 2022 EdgeImpulse Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

/* Includes ---------------------------------------------------------------- */

// #define HOSTNAME "esp32s3box"
#include <Arduino.h>
#include <task.h>
#include <queue.h>

#include <WiFi.h>
#include <WiFiClient.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

#include <MTJ-person-detection-ICT720Project_inferencing.h>
#include "edge-impulse-sdk/dsp/image/image.hpp"
#include "main.h"
#include "hw_camera.h"
#include "openmvrpc.h"
#include <iostream>
#include <ESPAsyncWebServer.h>
// #include <ctime>

// constants
#define TAG           "main"

#define BUTTON_PIN    0

#define MQTT_BROKER       "broker.hivemq.com"
#define MQTT_PORT         1883
#define HIVEMQ_USERNAME   "esp32_cam_test"
#define MQTT_PERSON_TOPIC  "esp32/park/cam/person/dev_A"
#define MQTT_CAMERA_TOPIC "esp32/park/cam/status"

#define WIFI_SSID ""
#define WIFI_PASSWORD ""

// global variables
WiFiClient wifi_client;
PubSubClient mqtt_client(wifi_client);
StaticJsonDocument<200> json_doc;

// queue handle
QueueHandle_t evt_queue;

/* Constant defines -------------------------------------------------------- */
#define EI_CAMERA_RAW_FRAME_BUFFER_COLS           320
#define EI_CAMERA_RAW_FRAME_BUFFER_ROWS           240
#define EI_CAMERA_FRAME_BYTE_SIZE                 3

/* Private variables ------------------------------------------------------- */
static bool debug_nn = false; // Set this to true to see e.g. features generated from the raw signal
static bool is_initialised = false;
uint8_t *snapshot_buf; //points to the output of the capture


/* Function definitions ------------------------------------------------------- */
bool ei_camera_init(void);
void ei_camera_deinit(void);
bool ei_camera_capture(uint32_t img_width, uint32_t img_height, uint8_t *out_buf) ;
static int ei_camera_get_data(size_t offset, size_t length, float *out_ptr);

AsyncWebServer server(80);

//ADDED
// static variables
static uint8_t jpg_buf[20480];
static uint16_t jpg_sz = 0;
static bool read_flag = false;

openmv::rpc_scratch_buffer<256> scratch_buffer;
openmv::rpc_callback_buffer<8> callback_buffer;
openmv::rpc_hardware_serial_uart_slave rpc_slave;

// static function declarations
static void print_memory(void);

size_t button_read_callback(void *out_data);
size_t jpeg_image_snapshot_callback(void *out_data);
size_t jpeg_image_read_callback(void *out_data);

// callback function when command is received
void on_cmd_received(char* topic, byte* payload, unsigned int length) {
  // ignored
}

/**
* @brief      Arduino setup function
*/
void setup()
{
    // put your setup code here, to run once:
    Serial.begin(115200);
    //comment out the below line to start inference immediately after upload
    while (!Serial);
    Serial.println("Edge Impulse Inferencing Demo");
    if (ei_camera_init() == false) {
        ei_printf("Failed to initialize Camera!\r\n");
        json_doc.clear();
        json_doc["camera"] = "off";
    }
    else {
        json_doc.clear();
        json_doc["camera"] = "on";
          // initialize serial and network
        Serial.begin(115200);
        WiFi.mode(WIFI_OFF);
        delay(100);
        WiFi.mode(WIFI_STA);
        delay(100);
        WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
        while (WiFi.status() != WL_CONNECTED) {
            delay(1000);
            Serial.println("Connecting to WiFi...");
        }
        // Print ESP Local IP Address
        Serial.println(" connected!");
        Serial.print("IP Address: ");
        Serial.println(WiFi.localIP());
        mqtt_client.setServer(MQTT_BROKER, MQTT_PORT);
        mqtt_client.setCallback(on_cmd_received);
        mqtt_client.connect(HIVEMQ_USERNAME);
        
        ei_printf("Camera initialized\r\n");
        rpc_slave.register_callback(F("button_read"), button_read_callback);
        rpc_slave.register_callback(F("jpeg_image_snapshot"), jpeg_image_snapshot_callback);
        rpc_slave.register_callback(F("jpeg_image_read"), jpeg_image_read_callback);
        rpc_slave.begin();

        // Start the web server
        server.on("/camera", HTTP_GET, [](AsyncWebServerRequest *request) {
            camera_fb_t * fb = NULL;
            fb = esp_camera_fb_get();
            if (!fb) {
                Serial.println("Camera capture failed");
                return;
            }

            // Convert the camera frame buffer to a String
            // Convert the camera frame buffer to a String
            String content(reinterpret_cast<const char*>(fb->buf), fb->len);

            // Send the camera feed to the client
            request->send(200, "image/jpeg", content);

            // Release the frame buffer
            esp_camera_fb_return(fb);
        });

        if (mqtt_client.connected())
        {
            mqtt_client.publish(MQTT_CAMERA_TOPIC, json_doc.as<String>().c_str());
        }


        server.begin();
        
    }

    ei_printf("\nStarting continious inference in 2 seconds...\n");
    ei_sleep(2000);
}

/**
* @brief      Get data and run inferencing
*
* @param[in]  debug  Get debug info if true
*/
void loop()
{
    int new_count = 0;
      // instead of wait_ms, we'll wait on the signal, this allows threads to cancel us...
    if (ei_sleep(5) != EI_IMPULSE_OK) {
        return;
    }

    snapshot_buf = (uint8_t*)malloc(EI_CAMERA_RAW_FRAME_BUFFER_COLS * EI_CAMERA_RAW_FRAME_BUFFER_ROWS * EI_CAMERA_FRAME_BYTE_SIZE);

    // check if allocation was successful
    if(snapshot_buf == nullptr) {
        ei_printf("ERR: Failed to allocate snapshot buffer!\n");
        return;
    }

    ei::signal_t signal;
    signal.total_length = EI_CLASSIFIER_INPUT_WIDTH * EI_CLASSIFIER_INPUT_HEIGHT;
    signal.get_data = &ei_camera_get_data;

    if (ei_camera_capture((size_t)EI_CLASSIFIER_INPUT_WIDTH, (size_t)EI_CLASSIFIER_INPUT_HEIGHT, snapshot_buf) == false) {
        ei_printf("Failed to capture image\r\n");
        free(snapshot_buf);
        return;
    }

    // Run the classifier
    ei_impulse_result_t result = { 0 };

    EI_IMPULSE_ERROR err = run_classifier(&signal, &result, debug_nn);
    if (err != EI_IMPULSE_OK) {
        ei_printf("ERR: Failed to run classifier (%d)\n", err);
        return;
    }

    // print the predictions
    ei_printf("Predictions (DSP: %d ms., Classification: %d ms., Anomaly: %d ms.): \n",
                result.timing.dsp, result.timing.classification, result.timing.anomaly);

#if EI_CLASSIFIER_OBJECT_DETECTION == 1
    new_count = 0;
    bool bb_found = result.bounding_boxes[0].value > 0;
    if (!bb_found)
    {
        ei_printf("    No objects found\n");
    }
    else{
        for (size_t ix = 0; ix < result.bounding_boxes_count; ix++) {
            auto bb = result.bounding_boxes[ix];
            if (bb.value == 0) {
                continue;
            }
            new_count++;
            // detect_count++;
            // json_doc.clear();
            // json_doc["status"] = "detected";
            // json_doc["timestamp"] = millis();
            // json_doc["detected"] = true;
            // json_doc["centroid_x"] = bb.x;
            // json_doc["centroid_y"] = bb.y;
            // json_doc["total"] = detect_count;
            // json_doc["Zone A"] = new_count;
            Serial.print("Detected in One Frame: ");
            Serial.println(new_count);
            ei_printf("    %s (%f) [ x: %u, y: %u, width: %u, height: %u ]\n", bb.label, bb.value, bb.x, bb.y, bb.width, bb.height);
        }
        // // current date/time based on current system
        // time_t now = time(0);
        
        // // convert now to string form
        // char* dt = ctime(&now);

        json_doc.clear();
        json_doc["capture"] = "detected";
        json_doc["location"] = "Zone A";
        // json_doc["time"] = dt;       use python to get local time instead
        json_doc["new_capture"] = new_count;
        if (mqtt_client.connected()) {
            mqtt_client.publish(MQTT_PERSON_TOPIC, json_doc.as<String>().c_str());
        }

        // Serial.print("The local date and time is: ");
        // Serial.print(dt);
        // Serial.println();
        Serial.print("New Capture In Zone A = ");
        Serial.print(new_count);
        Serial.println("------------------------------------------------------------\n\n");

    }
    // if (!bb_found) {
    //     ei_printf("    No objects found\n");
    // }
    // else{
    //     Serial.print("Zone A = ");
    //     Serial.print(new_count);
    //     Serial.println();
    // }
#else
    for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
        ei_printf("    %s: %.5f\n", result.classification[ix].label,
                                    result.classification[ix].value);
    }
#endif

#if EI_CLASSIFIER_HAS_ANOMALY == 1
        ei_printf("    anomaly score: %.3f\n", result.anomaly);
#endif
    // ADDED
    if (read_flag) {
        rpc_slave.put_bytes(jpg_buf, jpg_sz, 10000);
        read_flag = false;
    }
    rpc_slave.loop();
    free(snapshot_buf);
    // execute MQTT loop
    if (mqtt_client.connected()) {
        mqtt_client.loop();
        Serial.println("MQTT loop");
    } else {
        Serial.println("MQTT disconnected");
    }
    delay(2000);

}

/**
 * @brief   Setup image sensor & start streaming
 *
 * @retval  false if initialisation failed
 */
bool ei_camera_init(void) {

    if (is_initialised) return true;

// #if defined(CAMERA_MODEL_ESP_EYE)
  pinMode(9, INPUT_PULLUP);
  pinMode(8, INPUT_PULLUP);
// endif

    //initialize the camera
    esp_err_t err = esp_camera_init(&camera_config); //extern camera_config in hw_camera.h
    if (err != ESP_OK) {
      Serial.printf("Camera init failed with error 0x%x\n", err);
      return false;
    }

    sensor_t * s = esp_camera_sensor_get();
    // initial sensors are flipped vertically and colors are a bit saturated
    if (s->id.PID == OV3660_PID) {
      s->set_vflip(s, 1); // flip it back
      s->set_brightness(s, 1); // up the brightness just a bit
      s->set_saturation(s, 0); // lower the saturation
    }
// 3rd Commented
// #if defined(CAMERA_MODEL_M5STACK_WIDE)
//     s->set_vflip(s, 1);
//     s->set_hmirror(s, 1);
// #if defined(CAMERA_MODEL_ESP_EYE)
    s->set_vflip(s, 1);
    s->set_hmirror(s, 1);
    s->set_awb_gain(s, 1);
// #endif

    is_initialised = true;
    return true;
}

/**
 * @brief      Stop streaming of sensor data
 */
void ei_camera_deinit(void) {

    //deinitialize the camera
    esp_err_t err = esp_camera_deinit();

    if (err != ESP_OK)
    {
        ei_printf("Camera deinit failed\n");
        return;
    }

    is_initialised = false;
    return;
}


/**
 * @brief      Capture, rescale and crop image
 *
 * @param[in]  img_width     width of output image
 * @param[in]  img_height    height of output image
 * @param[in]  out_buf       pointer to store output image, NULL may be used
 *                           if ei_camera_frame_buffer is to be used for capture and resize/cropping.
 *
 * @retval     false if not initialised, image captured, rescaled or cropped failed
 *
 */
bool ei_camera_capture(uint32_t img_width, uint32_t img_height, uint8_t *out_buf) {
    bool do_resize = false;

    if (!is_initialised) {
        ei_printf("ERR: Camera is not initialized\r\n");
        return false;
    }

    camera_fb_t *fb = esp_camera_fb_get();

    if (!fb) {
        ei_printf("Camera capture failed\n");
        return false;
    }

   bool converted = fmt2rgb888(fb->buf, fb->len, PIXFORMAT_JPEG, snapshot_buf);

   esp_camera_fb_return(fb);

   if(!converted){
       ei_printf("Conversion failed\n");
       return false;
   }

    if ((img_width != EI_CAMERA_RAW_FRAME_BUFFER_COLS)
        || (img_height != EI_CAMERA_RAW_FRAME_BUFFER_ROWS)) {
        do_resize = true;
    }

    if (do_resize) {
        ei::image::processing::crop_and_interpolate_rgb888(
        out_buf,
        EI_CAMERA_RAW_FRAME_BUFFER_COLS,
        EI_CAMERA_RAW_FRAME_BUFFER_ROWS,
        out_buf,
        img_width,
        img_height);
    }


    return true;
}

static int ei_camera_get_data(size_t offset, size_t length, float *out_ptr)
{
    // we already have a RGB888 buffer, so recalculate offset into pixel index
    size_t pixel_ix = offset * 3;
    size_t pixels_left = length;
    size_t out_ptr_ix = 0;

    while (pixels_left != 0) {
        out_ptr[out_ptr_ix] = (snapshot_buf[pixel_ix] << 16) + (snapshot_buf[pixel_ix + 1] << 8) + snapshot_buf[pixel_ix + 2];

        // go to the next pixel
        out_ptr_ix++;
        pixel_ix+=3;
        pixels_left--;
    }
    // and done!
    return 0;
}

//ADDED
// Print memory information
// void print_memory() {
//   ESP_LOGI(TAG, "Total heap: %u", ESP.getHeapSize());
//   ESP_LOGI(TAG, "Free heap: %u", ESP.getFreeHeap());
//   ESP_LOGI(TAG, "Total PSRAM: %u", ESP.getPsramSize());
//   ESP_LOGI(TAG, "Free PSRAM: %d", ESP.getFreePsram());
// }

// callback for digital_read
size_t button_read_callback(void *out_data) {
  uint8_t state = 1;

  state = !digitalRead(BUTTON_PIN);
  memcpy(out_data, &state, sizeof(state));
  return sizeof(state);
}

// take camera snapshot
size_t jpeg_image_snapshot_callback(void *out_data) {
  jpg_sz = hw_camera_jpg_snapshot(jpg_buf);
  memcpy(out_data, &jpg_sz, sizeof(jpg_sz));
  return sizeof(jpg_sz);
}

// start reading image
size_t jpeg_image_read_callback(void *out_data) {
  read_flag = true;
  return 0;
}


#if !defined(EI_CLASSIFIER_SENSOR) || EI_CLASSIFIER_SENSOR != EI_CLASSIFIER_SENSOR_CAMERA
#error "Invalid model for current sensor"
#endif

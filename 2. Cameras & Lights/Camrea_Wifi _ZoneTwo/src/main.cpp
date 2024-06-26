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
// #define WIFI_SSID "AndroidAP3D06"
// #define WIFI_PASS "dapy6319"
// #define HOSTNAME "esp32s3box"

#include <person-detection_inferencing.h>
#include "edge-impulse-sdk/dsp/image/image.hpp"
#include "main.h"
#include "hw_camera.h"
#include "openmvrpc.h"
#include <iostream>
#include <WiFi.h>



// constants
#define TAG           "main"

#define BUTTON_PIN    0


#include <PubSubClient.h>

const char* ssid = "Tz";
const char* password = "123123123";
// MQTT Broker
const char* mqtt_broker = "172.20.10.4"; // The IP address of your Mosquitto broker
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  // Connect to Wi-Fi
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print("*");
  }

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println(message);

  //if (message == "ON") {
    //digitalWrite(LED_PIN, HIGH); // Turn the LED on
    //Serial.println("LED turned ON");
  //} else if (message == "OFF") {
    //digitalWrite(LED_PIN, LOW); // Turn the LED off
    //Serial.println("LED turned OFF");
  //}
  //Serial.println();
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP32_S3_Box_ZoneTwo_Client")) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("esp32_S3_Box_ZoneTwo", "esp32_S3_Box_ZoneTwo  is connected"); // Just one time when device is connected
      // ... and resubscribe
      //client.subscribe("esp32_S3_Box");
      
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}



// 1st comment
// #define CAMERA_MODEL_ESP_EYE

// //#if defined(CAMERA_MODEL_ESP_EYE)
// #define CAM_PWDN_PIN     -1
// #define CAM_RESET_PIN    18
// #define CAM_XCLK_PIN     14

// #define CAM_SIOD_PIN     4
// #define CAM_SIOC_PIN     5

// #define CAM_Y9_PIN       15
// #define CAM_Y8_PIN       16
// #define CAM_Y7_PIN       17
// #define CAM_Y6_PIN       12
// #define CAM_Y5_PIN       10
// #define CAM_Y4_PIN       8
// #define CAM_Y3_PIN       9
// #define CAM_Y2_PIN       11

// #define CAM_VSYNC_PIN    6
// #define CAM_HREF_PIN     7
// #define CAM_PCLK_PIN     13
//#endif

// Select camera model - find more camera models in camera_pins.h file here
// https://github.com/espressif/arduino-esp32/blob/master/libraries/ESP32/examples/Camera/CameraWebServer/camera_pins.h

// #define CAMERA_MODEL_ESP_EYE // Has PSRAM
// //#define CAMERA_MODEL_AI_THINKER // Has PSRAM

// #if defined(CAMERA_MODEL_ESP_EYE)
// #define PWDN_GPIO_NUM    -1
// #define RESET_GPIO_NUM   18
// #define XCLK_GPIO_NUM    4
// #define SIOD_GPIO_NUM    18
// #define SIOC_GPIO_NUM    23

// #define Y9_GPIO_NUM      36
// #define Y8_GPIO_NUM      37
// #define Y7_GPIO_NUM      38
// #define Y6_GPIO_NUM      39
// #define Y5_GPIO_NUM      35
// #define Y4_GPIO_NUM      14
// #define Y3_GPIO_NUM      13
// #define Y2_GPIO_NUM      34
// #define VSYNC_GPIO_NUM   5
// #define HREF_GPIO_NUM    27
// #define PCLK_GPIO_NUM    25

// #elif defined(CAMERA_MODEL_AI_THINKER)
// #define PWDN_GPIO_NUM     32
// #define RESET_GPIO_NUM    -1
// #define XCLK_GPIO_NUM      0
// #define SIOD_GPIO_NUM     26
// #define SIOC_GPIO_NUM     27

// #define Y9_GPIO_NUM       35
// #define Y8_GPIO_NUM       34
// #define Y7_GPIO_NUM       39
// #define Y6_GPIO_NUM       36
// #define Y5_GPIO_NUM       21
// #define Y4_GPIO_NUM       19
// #define Y3_GPIO_NUM       18
// #define Y2_GPIO_NUM        5
// #define VSYNC_GPIO_NUM    25
// #define HREF_GPIO_NUM     23
// #define PCLK_GPIO_NUM     22

// #else
// #error "Camera model not selected"
// #endif

/* Constant defines -------------------------------------------------------- */
#define EI_CAMERA_RAW_FRAME_BUFFER_COLS           320
#define EI_CAMERA_RAW_FRAME_BUFFER_ROWS           240
#define EI_CAMERA_FRAME_BYTE_SIZE                 3

/* Private variables ------------------------------------------------------- */
static bool debug_nn = false; // Set this to true to see e.g. features generated from the raw signal
static bool is_initialised = false;
uint8_t *snapshot_buf; //points to the output of the capture

// 2nd Comment
// static camera_config_t camera_config = {
//     .pin_pwdn=CAM_PWDN_PIN,
//     .pin_reset=CAM_RESET_PIN,
//     .pin_xclk=CAM_XCLK_PIN,
//     .pin_sscb_sda=CAM_SIOD_PIN,
//     .pin_sscb_scl=CAM_SIOC_PIN,

//     .pin_d7=CAM_Y9_PIN,
//     .pin_d6=CAM_Y8_PIN,
//     .pin_d5=CAM_Y7_PIN,
//     .pin_d4=CAM_Y6_PIN,
//     .pin_d3=CAM_Y5_PIN,
//     .pin_d2=CAM_Y4_PIN,
//     .pin_d1=CAM_Y3_PIN,
//     .pin_d0=CAM_Y2_PIN,
//     .pin_vsync=CAM_VSYNC_PIN,
//     .pin_href=CAM_HREF_PIN,
//     .pin_pclk=CAM_PCLK_PIN,
    
//     .xclk_freq_hz=20000000,
//     .ledc_timer=LEDC_TIMER_0,
//     .ledc_channel=LEDC_CHANNEL_0,
    
//     .pixel_format=PIXFORMAT_JPEG,
//     .frame_size = FRAMESIZE_QVGA,

//     .jpeg_quality = 12, //0-63 lower number means higher quality
//     .fb_count = 1,       //if more than one, i2s runs in continuous mode. Use only with JPEG
//     .fb_location = CAMERA_FB_IN_PSRAM,
//     .grab_mode = CAMERA_GRAB_WHEN_EMPTY,
    
// };


/* Function definitions ------------------------------------------------------- */
bool ei_camera_init(void);
void ei_camera_deinit(void);
bool ei_camera_capture(uint32_t img_width, uint32_t img_height, uint8_t *out_buf) ;
static int ei_camera_get_data(size_t offset, size_t length, float *out_ptr);

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



/**
* @brief      Arduino setup function
*/
void setup()
{
    // put your setup code here, to run once:
    Serial.begin(115200);

    setup_wifi();
    client.setServer(mqtt_broker, mqtt_port);
    client.setCallback(callback);

    //comment out the below line to start inference immediately after upload
    while (!Serial);
    Serial.println("Edge Impulse Inferencing Demo");
    if (ei_camera_init() == false) {
        ei_printf("Failed to initialize Camera!\r\n");
    }
    else {
        ei_printf("Camera initialized\r\n");
        rpc_slave.register_callback(F("button_read"), button_read_callback);
        rpc_slave.register_callback(F("jpeg_image_snapshot"), jpeg_image_snapshot_callback);
        rpc_slave.register_callback(F("jpeg_image_read"), jpeg_image_read_callback);
        rpc_slave.begin();

        
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
    if (!client.connected()) {
    reconnect();
    }
  client.loop();

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
    bool bb_found = result.bounding_boxes[0].value > 0;

    int counter = 0;

    for (size_t ix = 0; ix < result.bounding_boxes_count; ix++) {
        auto bb = result.bounding_boxes[ix];
        if (bb.value == 0) {
            continue;
        }
        counter++;

        ei_printf("    %s (%f) [ x: %u, y: %u, width: %u, height: %u ]\n", bb.label, bb.value, bb.x, bb.y, bb.width, bb.height);
    }
    if(counter !=0){
      ei_printf("detect %u persons", counter);
    char message[50]; // Assuming 50 characters would suffice for your message
    sprintf(message, "%u", counter); // Convert count to string
    client.publish("esp32_S3_Box_ZoneTwo/cam/detect", message);

    }
    else{
        client.publish("esp32_S3_Box_ZoneTwo/cam/detect", "0");
    } 
    if (!bb_found) {
        ei_printf("    No objects found\n");
    }
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
# AI Box Demo README

## About AI Box Demo
This showcases how the EdgeAI SDK can be modified to receive remote streams over UDP, one of the most common methods of sending data over the network and also a custom post process for the same inference. This workflow can be used to inference on feeds from IP enabled cameras and run much larger models on the server. In the example provided, the server simply logs the data it receives but more advanced things can be done as needed.

This demo uses the yolox-nano-lite model available on EdgeAI Model Zoo. Transfer learning was applied to the model to output two categories: occupied parking space and free parking space.

[!Demo Preview](https://github.com/user-attachments/assets/f5a869d6-877b-48d9-9d36-39b56e49cc66)

## Running the Demo
1. Copy the `apps_python` directory in the repo to the path `/opt/edgeai-gst-apps/apps_python` on the AM62A board.
2. Copy the `custom_models` directory in the repo to the path `/opt/custom_models` on the AM62A board.
3. Copy the `configs/udp_example.yaml` file in the repo to the path `/opt/edgeai-gst-apps/configs/udp_example.yaml` on the AM62A board.
4. Setup a python environment with flask installed on the PC and run the server (run in `server_example` directory):
    ```bash
    pip install -r requirements.txt
    python3 app_server.py
    ```
5. On the AM62P, run the following command:
    ```bash
    gst-launch-1.0 v4l2src device=<USB Camera Device> io-mode=2 ! image/jpeg, width=1280, height=720 ! rtpjpegpay ! udpsink host=<AM62A Device IP> port=5000 sync=false
    ```
6. On the AM62A, run the following command:
    ```bash
    export SERVER_IP="<HOST IP>"
    export SERVER_PORT=5000 //Default port configured in the server. Change accordingly
    ./apps_python/app_edgeai.py configs/udp_example.yaml
    ```
Replace the values in angle brackets with the correct values. To get IP addresses, `ifconfig` command can be used. It should also be noted that all three devices should be on the same network

## Result
The application has two main parts: A live feed and the server. The live video is overlaid with the bounding boxes of each parking space and the counts of occupied and free parking spaces. The green boxes represent occupied spaces and the red boxes represent free spaces. The server receives the data from the EVM and displays it on a frontend. The application sends data to a remote HTTP server. We can send get requests to the example server and it responds with a html file displaying all the data it has received.

## Overview of Changes
The demo made the following changes to the EdgeAI SDK to support this workflow (Corresponding commits are also linked to understand the modifications done):
1. UDP input support was added to the SDK. This also requires waiting for the stream initially. ([Commit that adds UDP input support](https://github.com/goyal-jay/edgeai-gst-apps-aibox/commit/7d935f1af22b028dd5f3bedabef61a1a67eeb2c3), [Commit that adds jpeg support over UDP](https://github.com/goyal-jay/edgeai-gst-apps-aibox/commit/f722c7122b53d840ca8acdba91d2fd1bb0a5c0f2))

2. A custom post processing script was added along with a corresponding server. ([Corresponding commit](https://github.com/goyal-jay/edgeai-gst-apps-aibox/commit/7d935f1af22b028dd5f3bedabef61a1a67eeb2c3))

## Reference
This demo uses the PKLot dataset available [here](https://web.inf.ufpr.br/vri/databases/parking-lot-database/). This dataset(licensed under [CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/)) was introduced in the following paper: _[Almeida, P., Oliveira, L. S., Silva Jr, E., Britto Jr, A., Koerich, A., PKLot – A robust dataset for parking lot classification, Expert Systems with Applications, 42(11):4937-4949, 2015.](https://www.inf.ufpr.br/lesoliveira/download/ESWA2015.pdf)_

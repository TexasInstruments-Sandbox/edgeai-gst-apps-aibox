# AI Box Demo README

# Running the Demo
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

**Tested On: AM62A running SDK v10.0**

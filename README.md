# PingerGUI

PingerGUI is a versatile GUI-based ping utility developed using the Python Flet framework and the `ping3` library. It allows you to ping multiple IP addresses simultaneously and view their real-time status and statistics.

## 🚀 Features

* **Support for Multiple Destination IP Addresses:** Ping several IP addresses concurrently.
* **Flexible IP Address Input:**
    * Single IP addresses (e.g., `192.168.1.1`)
    * IP address ranges (e.g., `192.168.1.1-10`)
    * CIDR notation (e.g., `192.168.1.0/24`)
    * Comma-separated lists (e.g., `192.168.1.1,192.168.1.5`)
    * Combinations of the above are also supported.
* **Detailed Ping Configuration:**
    * **Timeout:** The timeout duration for each ping request (in seconds).
    * **Interval:** The waiting time between each ping request (in milliseconds).
    * **TTL (Time To Live):** The maximum number of hops a packet can traverse through routers.
    * **Packet Size:** The size of the ping packet to send.
* **Real-time Result Display:**
    * Sent Count
    * Received Count
    * Last Response Time
* **Start/Stop Ping:** Control ping operations with dedicated buttons.
* **Reset Statistics:** Clear statistics for individual destinations.

## ⚙️ Requirements

* Python 3.8 or newer
* Flet library
* ping3 library

## 📦 Installation

1.  Clone this repository:

    ```bash
    git clone [https://github.com/your_username/PingerGUI.git](https://github.com/your_username/PingerGUI.git)
    cd PingerGUI
    ```

2.  Install the required libraries directly:

    ```bash
    pip install flet ping3
    ```

## 🚀 Usage

1.  Run the application:

    ```bash
    python main.py
    ```

2.  The GUI window will appear.
3.  Click the **"Add to Destination List" button** to enter the IP addresses you wish to ping. Various input formats are supported.
4.  Click the **"Settings" button** to configure ping parameters such as timeout, interval, TTL, and packet size.
5.  Click the **"Run" button** to start pinging. Real-time ping results for each destination will be displayed.
6.  Click the **"Stop" button** to halt the ping process.
7.  Use the **"Clear" button** next to each destination to reset its statistics.

# Simple Reverse Shell 

**Warning: This script is for educational purposes only and is highly insecure. Do not use it in production or against systems you do not own. It contains significant security vulnerabilities, particularly a shell injection vulnerability.**

This Python script creates a basic reverse shell server that listens for incoming connections and allows a connected client to execute commands on the server's operating system.

## Features

*   **Multi-threaded:** Handles multiple client connections concurrently using threads.
*   **Command Execution:** Executes commands received from clients on the server's shell.
*   **Exit Command:** Clients can send the `exit` command to gracefully close their connection.
*   **Simple Command-Line Interface:** Uses `click` to easily specify the listening port.

## Usage

### Running the Server

1.  **Clone the repository (or download the script):**

    ```bash
    git clone https://github.com/DilanM818/Reverse_Shell
    cd Reverse_Shell
    ```

2.  **Make the script executable (if necessary):**

    ```bash
    chmod +x reverse_shell.py
    ```

3.  **Run the server:**

    ```bash
    ./reverse_shell.py
    ```

    You can optionally specify a different port using the `-p` or `--port` option:

    ```bash
    ./reverse_shell.py -p 8080
    # or
    ./reverse_shell.py --port 8080
    ```

    The server will start listening for connections on the specified port (default: 4444).

### Connecting as a Client

You can use `netcat` or a similar tool to connect to the server as a client.

**Using `netcat` (nc):**

1.  **On your client machine, open a terminal and use `netcat` to connect to the server's IP address and port:**

    ```bash
    nc <server_ip> <server_port>
    ```

    Replace `<server_ip>` with the IP address of the machine running the server script, and `<server_port>` with the port the server is listening on (e.g., 4444 or 8080 if you changed it).

2.  **Once connected, you can type commands and press Enter to send them to the server.** The output of the command executed on the server will be displayed in your client terminal.

3.  **To close the connection from the client side, type `exit` and press Enter.**



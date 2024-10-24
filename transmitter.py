# transmitter.py

import socket
import json
import time
import logging
import os
from datetime import datetime
from rich.console import Console
from rich.progress import track
from shannon_fano import shannon_fano_encoder, get_symbol_frequencies

HOST = 'localhost'
PORT = 12345

console = Console()

# Function to clear the terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Clear terminal at the start of each session
clear_terminal()

# Create logs directory with session time
session_time = datetime.now().strftime('%Y%m%d_%H%M%S')
log_dir = f"logs/{session_time}"
os.makedirs(log_dir, exist_ok=True)

# Configure logging to log file in the session directory
log_filename = f"{log_dir}/transmitter.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_and_show_encoding_process(message, encoding_table):
    console.print("\n[bold yellow]Encoding process:[/bold yellow]")
    for char in message:
        encoded_bits = encoding_table[char]
        console.print(f"[green]Character '{char}' -> [bold cyan]{encoded_bits}[/bold cyan]", highlight=True)
        logging.info(f"Character '{char}' encoded to '{encoded_bits}'")
        time.sleep(0.5)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        console.print("[bold blue]Connected to receiver.[/bold blue]\n")
        logging.info("Connected to receiver.")
        
        while True:
            message = input("Enter message to send (or 'exit' to quit): ")
            if message == 'exit':
                s.sendall(b'exit')
                logging.info("Transmission ended by user.")
                break
            
            frequencies = get_symbol_frequencies(message)
            encoding_table = shannon_fano_encoder(frequencies)
            encoded_message = ''.join([encoding_table[char] for char in message])
            
            # Log the original message and encoded message
            logging.info(f"Original message: {message}")
            logging.info(f"Encoded message: {encoded_message}")
            
            # Show step-by-step encoding process and log it
            log_and_show_encoding_process(message, encoding_table)
            console.print(f"\n[bold magenta]Final encoded message:[/bold magenta] {encoded_message}\n")
            
            # Simulate sending with progress bar
            console.print("\n[bold yellow]Sending message...[/bold yellow]\n")
            for _ in track(range(10), description="Sending..."):
                time.sleep(0.1)
            
            # Send the encoded message and encoding table
            s.sendall(encoded_message.encode('utf-8'))
            s.sendall(json.dumps(encoding_table).encode('utf-8'))
            logging.info("Message and encoding table sent.")
            
            console.print("\n[bold green]Message sent![/bold green]\n")  # Add a new line after each message

if __name__ == "__main__":
    main()

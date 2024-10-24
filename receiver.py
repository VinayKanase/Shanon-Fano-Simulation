# receiver.py

import socket
import json
import time
import logging
import os
from datetime import datetime
from rich.console import Console
from rich.progress import track
from shannon_fano import shannon_fano_decoder

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

# Corrected logging configuration
log_filename = f"{log_dir}/receiver.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')  

def log_and_show_decoding_process(encoded_message, encoding_table):
    console.print("\n[bold yellow]Decoding process:[/bold yellow]")
    current_code = ""
    for bit in encoded_message:
        current_code += bit
        if current_code in encoding_table.values():
            char = [k for k, v in encoding_table.items() if v == current_code][0]
            console.print(f"[cyan]Bits '{current_code}' -> [bold green]Character '{char}'[/bold green]", highlight=True)
            logging.info(f"Bits '{current_code}' decoded to character '{char}'")
            current_code = ""
        time.sleep(0.5)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        console.print("[bold blue]Receiver is waiting for connections...[/bold blue]\n")
        logging.info("Receiver is waiting for connections.")
        conn, addr = s.accept()
        
        with conn:
            console.print(f"[bold green]Connected by {addr}[/bold green]\n")
            logging.info(f"Connected by {addr}.")
            while True:
                encoded_msg = conn.recv(1024).decode('utf-8')
                if encoded_msg == 'exit':
                    console.print("[bold red]Transmission ended.[/bold red]\n")
                    logging.info("Transmission ended.")
                    break
                
                encoding_table_str = conn.recv(1024).decode('utf-8')
                encoding_table = json.loads(encoding_table_str)
                
                console.print(f"\n[bold magenta]Encoded message received:[/bold magenta] {encoded_msg}\n")
                logging.info(f"Encoded message received: {encoded_msg}")
                
                # Simulate receiving with progress bar
                console.print("\n[bold yellow]Receiving message...[/bold yellow]\n")
                for _ in track(range(10), description="Receiving..."):
                    time.sleep(0.1)
                
                # Show decoding process and log it
                log_and_show_decoding_process(encoded_msg, encoding_table)
                
                decoded_message = shannon_fano_decoder(encoded_msg, encoding_table)
                console.print(f"\n[bold green]Decoded message:[/bold green] {decoded_message}\n")
                logging.info(f"Decoded message: {decoded_message}")
                
                console.print("\n[bold green]Message received and decoded![/bold green]\n")  # Add new lines for clarity

if __name__ == "__main__":
    main()

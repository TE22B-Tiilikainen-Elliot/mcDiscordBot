import discord
import socket
import asyncio

TOKEN = ""
CHANNEL_ID = 1228685869431521374  # Replace with your channel ID
SERVER_IP = "151.177.19.118"
SERVER_PORT = 25566

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def check_server():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    last_status = False  # Track last known status to avoid spamming
    
    while not client.is_closed():
        is_open = check_port(SERVER_IP, SERVER_PORT)

        if is_open and not last_status:  # Only send message when status changes
            await channel.send("Server is open!, at "+SERVER_IP+":"+str(SERVER_PORT))
        
        last_status = is_open
        await asyncio.sleep(60)  # Wait 1 minute before checking again

def check_port(ip, port):
    """Check if the port is open"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(3)  # Timeout after 3 seconds
        return s.connect_ex((ip, port)) == 0

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    client.loop.create_task(check_server())  # Start the checking loop

client.run(TOKEN)
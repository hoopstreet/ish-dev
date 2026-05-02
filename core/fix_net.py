import socket
try:
    socket.create_connection(("149.154.167.50", 443), timeout=5)
    print("✅ Connection to Telegram successful!")
except Exception as e:
    print(f"❌ Connection Failed: {e}")

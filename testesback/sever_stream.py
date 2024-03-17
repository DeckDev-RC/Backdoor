from vidstream import StreamingServer

server = StreamingServer("10.0.0.219", 4444)
server.start_server()

while input("command:>") != "stop":
    continue

server.stop_server()
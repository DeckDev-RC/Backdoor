from vidstream import ScreenShareClient

client = ScreenShareClient("10.0.0.219", 4444)
client.start_stream()
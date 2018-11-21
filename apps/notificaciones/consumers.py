from channels.consumer import AsyncConsumer
# Create your views here.

class EchoConsumer(AsyncConsumer):
	async def websocket_connect(self, event):
		await self.send({
			"type": "websocket.accept"
			})

	async def websocket_receive(self, event):
		await self.send({
			"type": "websocket.send",
			"text": event["text"]
			})
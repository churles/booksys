from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="sender")
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="receiver")
	message = models.TextField()
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('sender',)

	def __str__(self):
		return str(self.sender)
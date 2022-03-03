from asyncio.windows_events import NULL
from django import template
from reviews.models import Review, ReviewLike
from books.models import Book
from accounts.models import Profile

register=template.Library()

@register.simple_tag
def counter(args):
	if args == 1:
		return "break"

@register.simple_tag
def profile(args):
	profile = "/media/3.png"
	if Profile.objects.filter(account=args):
		profile = Profile.objects.filter(account=args)[0]
		profile = profile.picture.url
	return profile
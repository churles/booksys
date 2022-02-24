from asyncio.windows_events import NULL
from django import template
from reviews.models import Review, ReviewLike
from books.models import Book

register=template.Library()

@register.simple_tag
def counter(args):
	if args == 1:
		return "break"

from asyncio.windows_events import NULL
from django import template
from reviews.models import Review, ReviewLike
from books.models import Book

register=template.Library()

@register.simple_tag
def total_review():
	return Review.objects.count()

@register.simple_tag
def total_like(args):
	review = Review.objects.get(id = args)
	return ReviewLike.objects.filter(review=review).count()

@register.simple_tag
def counter(args):
	if args == 1:
		return "break"

@register.simple_tag
def checker(args, args1):
	review = Review.objects.get(id=args)
	likes = ReviewLike.objects.filter(review=review, owner=args1)
	return likes


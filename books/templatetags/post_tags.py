from asyncio.windows_events import NULL
from django import template
from reviews.models import Review, ReviewLike
from books.models import Book
import datetime 

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

@register.simple_tag
def dateRented(args):
	date_1 = datetime.datetime.strptime(str(args), "%Y-%m-%d %H:%M:%S%z")
	end_date = datetime.datetime.strftime(date_1, "%b. %d, %Y")
	return end_date

@register.simple_tag
def returnDate(args, args1):
	date_1 = datetime.datetime.strptime(str(args), "%Y-%m-%d %H:%M:%S%z")
	end_date = date_1 + datetime.timedelta(days=int(args1)+7)
	end_date = datetime.datetime.strftime(end_date, "%b. %d, %Y")
	return end_date

@register.simple_tag
def dateCounter(args, args1):
	date_1 = datetime.datetime.strptime(str(args), "%Y-%m-%d %H:%M:%S%z")
	end_date = date_1 + datetime.timedelta(days=int(args1)+7)
	counter = end_date - date_1
	return str(counter).strip(', 0:00:00')
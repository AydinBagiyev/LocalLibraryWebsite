from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
# Create your views here.

def index(request):
	'''
	View function for home page of site.
	'''
	# Generate counts of the some main objects.

	number_books = Books.objects.all().count();
	number_instances = BookInstance.objects.all().count();

	# Available books (status = 'a')
	number_instances_available = BookInstance.objects.filter(status__exact='a').count();
	number_authors = Author.objects.count(); # The 'all()' is implied by default.

	# Render the index.html with the data in the index variable

	return request(
		request,
		'index.html',
		context={'number_books':number_books, 'number_instances':number_instances, 'number_instances_available':number_instances_available, 'number_authors':number_authors}
		)

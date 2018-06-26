from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
# Create your views here.

def index(request):
	'''
	View function for home page of site.
	'''
	# Generate counts of the some main objects.

	number_books = Book.objects.all().count();
	number_instances = BookInstance.objects.all().count();

	# Available books (status = 'a')
	number_instances_available = BookInstance.objects.filter(status__exact='a').count();
	number_authors = Author.objects.count(); # The 'all()' is implied by default.

	# Filtering genre and get amount of it.
	number_genre = Genre.objects.filter(name__icontains = 's')

	# Number of visits to this view, as counted in the session variable.
	number_visits = request.session.get('number_visits', 0)
	request.session['number_visits'] = number_visits + 1

	# Render the index.html with the data in the index variable

	return render(
		request,
		'index.html',
		context={'number_books':number_books, 'number_instances':number_instances, 'number_instances_available':number_instances_available, 'number_authors':number_authors, 'number_genre': number_genre,
		'number_visits': number_visits}
		)


from django.views import generic

class BookListView(generic.ListView):
	model = Book
	paginate_by = 10

	# context_object_name = 'my_book_list' # your own name for  the list as a template variable
	# queryset = Book.objects.filter(title__icontains ='war')[:5] # Getting 5 books containing the title war
	# template_name = 'book/my_arbitrary_template_name_list.html' # Specify your own template name/location  

	# def get_queryset(self):
	# 	return Book.objects.filter(title__icontains ='war')[:5] # Getting 5 books containing the title war

	# def get_context_data(self, **kwargs):
	# 	# Get the base implementation to get the context
	# 	context = super(BookListView, self).get_context_data(**kwargs)
	# 	# Create any data and add it to the context
	# 	context['some data'] = 'This is just some data'
	# 	return context

class BookDetailView(generic.DetailView):
	model = Book

class AuthorListView(generic.ListView):
	model = Author

class AuthorDetailView(generic.DetailView):
	model = Author

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
	'''
	Generic class-based view listing books on loan to current user.
	'''

	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='0').order_by('due_back')
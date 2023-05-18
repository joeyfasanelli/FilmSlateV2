from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from.models import MovieReview, TvReview, Reaction, Movie
import requests

#TMBD_API_KEY = "27866702f39bce28cfa7752a49f16399"


# API Search Query with TMDB API


def search(request):
  query = request.GET.get('q')

  if query:
    data = requests.get(f"https://api.themoviedb.org/3/search/{request.GET.get('type')}?api_key=27866702f39bce28cfa7752a49f16399&language=en-US&page=1&include_adult=false&query={query}")


  else:
    return HttpResponse("Please enter a search query")
  
  return render(request, "results.html", {'data': data.json(), "type": request.GET.get('type')})




# APP ROUTES

def home(request):
    return render(request, 'home.html')



def about(request):
    return render(request, 'about.html')



def view_tv_detail(request, tv_id):
  data = requests.get(f"https://api.themoviedb.org/3/tv/{tv_id}?api_key=27866702f39bce28cfa7752a49f16399&language=en-US")
  return render(request, 'tv_detail.html', {'data': data.json()})



def view_movie_detail(request, movie_id):
  data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=27866702f39bce28cfa7752a49f16399&language=en-US")
  return render(request, 'movie_detail.html', {'data': data.json()})



def view_trending_results(request):
  type = request.GET.get('type') if request.GET.get('type') else "all"
  trendings = requests.get(f"https://api.themoviedb.org/3/trending/{type}/week?api_key=27866702f39bce28cfa7752a49f16399&language=en-US")
  return JsonResponse(trendings.json())


@login_required
def review_page_movie(request, movie_id):
  if request.method == "POST":
    user = request.user
    movie_review = request.POST.get("review")

    if not request.user.is_authenticated:
      user = User.objects.get(id=1)

    MovieReview(movie_review=movie_review, user=user, movie_id=movie_id).save()

    return redirect(f"/movie/{movie_id}/review")
  
  else:
    data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=27866702f39bce28cfa7752a49f16399&language=en-US")
    title = data.json()["title"]

    reviews = reversed(MovieReview.objects.filter(movie_id=movie_id))

    return render(request, "movie_reviews.html", {"title": title, "reviews": reviews})



@login_required
def review_page_tv(request, tv_id):
  if request.method == "POST":
    user = request.user
    tv_review = request.POST.get("review")

    if not request.user.is_authenticated:
      user = User.objects.get(id=1)

    TvReview(tv_review=tv_review, user=user, tv_id=tv_id).save()

    return redirect(f"/tv/{tv_id}/reviews")
  
  else:
    data = requests.get(f"https://api.themoviedb.org/3/tv/{tv_id}?api_key=27866702f39bce28cfa7752a49f16399&language=en-US")
    name = data.json()["name"]

    reviews = reversed(TvReview.objects.filter(tv_id=tv_id))

    return render(request, "tv_reviews.html", {"name": name, "reviews": reviews})


@login_required
def assoc_reaction(request, movie_id, reaction_id):
  Movie.objects.get(id=movie_id).reactions.add(reaction_id)
  return redirect('detail', movie_id=movie_id)

@login_required
def movies_index(request):
    movies = Movie.objects.filter(user=request.user)
    return render(request, 'movies/index.html', {'movies': movies})

@login_required
def movies_detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    reactions_movie_doesnt_have = Reaction.objects.exclude(id__in = movie.reactions.all().values_list('id'))
    return render(request, 'movies/detail.html', { 'movie': movie, 'reactions': reactions_movie_doesnt_have })

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up, please try again.'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)




class MovieCreate(LoginRequiredMixin, CreateView):
    model = Movie
    fields = ['title', 'description']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class TvReviewUpdate(LoginRequiredMixin, UpdateView):
  model = TvReview
  fields = ['tv_review']
  success_url ='/'

class MovieReviewUpdate(LoginRequiredMixin, UpdateView):
  model = MovieReview
  fields = ['movie_review']
  success_url = '/'

class TvReviewDelete(LoginRequiredMixin, DeleteView):
  model = TvReview
  success_url = '/'

class MovieReviewDelete(LoginRequiredMixin, DeleteView):
  model = MovieReview
  success_url = '/'

class MovieUpdate(LoginRequiredMixin, UpdateView):
  model = Movie
  fields = ['title', 'description']

class MovieDelete(LoginRequiredMixin, DeleteView):
  model = Movie
  success_url = '/movies/'
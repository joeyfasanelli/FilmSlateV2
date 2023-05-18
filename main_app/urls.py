from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('tv/<int:tv_id>/', views.view_tv_detail, name="tvdetail"),
    path('movie/<int:movie_id>/', views.view_movie_detail, name="moviedetail"),
    path('about/', views.about, name='about'),
    # path('movies/', views.movies_index, name='index'),
    # path('movies/create/', views.MovieCreate.as_view(), name='movies_create'),
    # path('movies/<int:movie_id>/', views.movies_detail, name='detail'),
    # path('movies/<int:pk>/update/', views.MovieUpdate.as_view(), name='movies_update'),
    # path('movies/<int:pk>/delete/', views.MovieDelete.as_view(), name='movies_delete'),
    # path('movies/<int:movie_id>/assoc_reaction/<int:reaction_id>/', views.assoc_reaction, name='assoc_reaction'),

    path('movie/<int:movie_id>/review/', views.review_page_movie, name='review_page_movie'),
    path('tv/<int:tv_id>/reviews/', views.review_page_tv, name='review_page_tv'),
    path('api/trendings/', views.view_trending_results, name="trendings"),
    path('reviews/<int:pk>/update/', views.TvReviewUpdate.as_view(), name='tv_reviews_update'),
    path('reviews/<int:pk>/delete/', views.TvReviewDelete.as_view(), name='tv_reviews_delete'),
    path('review/<int:pk>/update/', views.MovieReviewUpdate.as_view(), name='movie_reviews_update'),
    path('review/<int:pk>/delete/', views.MovieReviewDelete.as_view(), name='movie_reviews_delete'),
    path('accounts/signup/', views.signup, name='signup'),
]
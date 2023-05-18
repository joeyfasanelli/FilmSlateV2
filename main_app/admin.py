from django.contrib import admin
from .models import MovieReview, TvReview, Reaction, Movie

admin.site.register(MovieReview)
admin.site.register(TvReview)
admin.site.register(Reaction)
admin.site.register(Movie)
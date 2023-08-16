import uuid

from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import (
    SearchVectorField,
    SearchQuery,
    SearchRank,
    TrigramSimilarity,
)
from django.db.models import F, Q

# Dado que el filter estaba con mucha logica se arma una nueva clase para extender queryset
class WineQuerySet(models.query.QuerySet):  # new
    def search(self, query):
        search_query = Q(Q(search_vector=SearchQuery(query)))
        return (
            self.annotate(
                variety_headline=SearchHeadline(F("variety"), SearchQuery(query)),
                winery_headline=SearchHeadline(F("winery"), SearchQuery(query)),
                description_headline=SearchHeadline(
                    F("description"), SearchQuery(query)
                ),
                search_rank=SearchRank(F("search_vector"), SearchQuery(query)),
            )
            .filter(search_query)
            .order_by("-search_rank", "id")
        )


class Wine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    points = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    variety = models.CharField(max_length=255)
    winery = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    # nota: Agregar el search_vector con el indice mejoro un x5 la performance en este ejemplo
    search_vector = SearchVectorField(null=True, blank=True)
    # agregamos object manager
    objects = WineQuerySet.as_manager()

    class Meta:
        indexes = [GinIndex(fields=["search_vector"], name="search_vector_index")]
        # indexes = [
        #     GinIndex(
        #         name="desc_winery_variety_gin_idx",
        #         fields=["description", "winery", "variety"],
        #         opclasses=["gin_trgm_ops", "gin_trgm_ops", "gin_trgm_ops"],
        #     )
        # ]

    def __str__(self):
        return f"{self.id}"


# Clase custom para el highlighting cuando se retornan los resultados de la base con los match
class SearchHeadline(models.Func):
    function = "ts_headline"
    output_field = models.TextField()
    template = "%(function)s(%(expressions)s, 'StartSel = <mark>, StopSel = </mark>, HighlightAll=TRUE')"


class WineSearchWordQuerySet(models.query.QuerySet):
    def search(self, query):
        return (
            self.annotate(similarity=TrigramSimilarity("word", query))
            .filter(similarity__gte=0.3)
            .order_by("-similarity")
        )


# Let's begin by creating a database table to hold all of the unique words that appear in our Wine records
class WineSearchWord(models.Model):
    word = models.CharField(max_length=255, unique=True)
    objects = WineSearchWordQuerySet.as_manager()

    def __str__(self):
        return self.word

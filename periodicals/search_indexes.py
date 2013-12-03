import datetime
from haystack import indexes
from periodicals.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='issue__pub_date')
    # pregenerate the search result HTML for an Article
    # this avoids any database hits when results are processed
    # at the cost of storing all the data in the Haystack index
    result_text = indexes.CharField(indexed=False, use_template=True)

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(issue__pub_date__lte=datetime.datetime.now())

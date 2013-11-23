from haystack.sites import site
from haystack import indexes
from periodicals.models import Article


class ArticleIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='issue__pub_date')
    # pregenerate the search result HTML for an Article
    # this avoids any database hits when results are processed
    # at the cost of storing all the data in the Haystack index
    result_text = indexes.CharField(indexed=False, use_template=True)

site.register(Article, ArticleIndex)

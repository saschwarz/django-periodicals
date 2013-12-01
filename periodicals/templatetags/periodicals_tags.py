from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from periodicals.models import Article


register = template.Library()


def article_result(article, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    result = '''<p><div><a href="%s" class="result-title">%s</a></div><div class="article-result-series">%s</div>''' % (
        esc(article.get_absolute_url()),
        esc(article.title),
        esc(article.series))

    if article.description:
        result += '''<div class="result-desc">%s</div>''' % esc(article.description)

    result += '''<div class="result-issue-info">%s %s %s''' % (
        esc(article.issue.periodical.name),
        esc(article.issue.display_year()),
        esc(article.issue.display_name()))

    if article.page:
        result += " %s: %s" % (_("Page"),
                               esc(article.page))
    result += '</div>'
    authors = [esc(author.display_name()) for author in article.authors.all()]
    if authors:
        result += '''<div class="result-author">%s: %s</div>''' % (
            len(authors) > 1 and _("Authors") or _("Author"),
            ",".join(authors))

    if article.tags:
        result += '''<div class="result-tags">%s: %s</div>''' % (
            _("Tags"), article.tags.replace('"', ''))
    result += "</p>"
    return mark_safe(result)

article_result.needs_autoescape = True
register.filter('article_result', article_result)


def periodical_copyright(periodical, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    text = _('Titles, descriptions and images are copyright %(publisher)s and are used with permission.')
    result = text % (dict(publisher='''<a href="%s">%s</a>''' % (
                esc(periodical.website),
                esc(periodical.publisher))))
    return mark_safe(result)

periodical_copyright.needs_autoescape = True
register.filter('periodical_copyright', periodical_copyright)


class ArticleCountNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        return str(Article.objects.count())


def do_article_count(parser, token):
    return ArticleCountNode()

register.tag('article_count', do_article_count)

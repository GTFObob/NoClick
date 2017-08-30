from breadability.readable import Article, leaf_div_elements_into_paragraphs
from breadability.utils import cached_property
from lxml.html.clean import Cleaner

html_cleaner = Cleaner(
        scripts=True, javascript=True, comments=True,
        style=True, links=True, meta=False, add_nofollow=False,
        page_structure=False, processing_instructions=True,
        embedded=False, frames=False, forms=False,
        annoying_tags=False, remove_tags=None, kill_tags=("noscript", "iframe", "figcaption"),
        remove_unknown_tags=False, safe_attrs_only=False)

class CustomArticle(Article):
    ''' Customized Article that avoids certain tags '''

    @cached_property
    def dom(self):
        """Parsed lxml tree (Document Object Model) of the given html."""
        try:
            dom = self._original_document.dom
            # cleaning doesn't return, just wipes in place
            html_cleaner(dom)
            return leaf_div_elements_into_paragraphs(dom)
        except ValueError:
            return None
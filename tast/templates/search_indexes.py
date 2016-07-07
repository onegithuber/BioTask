from models  import Tast
from haystack import indexes
class TastIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    def get_model(self):
        return Tast
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

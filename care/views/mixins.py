class TitleMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "head": self.get_title
        })
        return context

    def get_title(self):
        return self.title

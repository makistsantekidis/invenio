from wtforms import IntegerField

__all__ = ['IntegerTextField']


class IntegerTextField(IntegerField):

    def __init__(self, **kwargs):
        super(IntegerTextField, self).__init__(**kwargs)

    def pre_validate(self):
            return dict(error=0, error_message='')

    def autocomplete(self):
        return []
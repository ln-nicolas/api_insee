from .field import Field

class FieldExact(Field):

    @property
    def representation(self):
        return '%s:"%s"' % (self.name, str(self.value))

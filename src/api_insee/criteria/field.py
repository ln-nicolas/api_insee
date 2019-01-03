from .base import Base

class Field(Base):


    def __init__(self, name, value, *args, **kwargs):
        self.name  = name
        self.value = value

    def toURLParams(self):
        query = self.representation

        if self.negative:
            query = '-'+query

        return query

    @property
    def representation(self):
        return '%s:%s' % (self.name, str(self.value))

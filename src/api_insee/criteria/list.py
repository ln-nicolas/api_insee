from .base import Base

class List(Base):

    def __init__(self, *criteria, **kwargs):
        self.criteria_list = criteria

    def toURLParams(self):
        return ' AND '.join([ ct.toURLParams() for ct in self.criteria_list ])

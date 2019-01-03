from .base import Base

class Periodic(Base):

    def __init__(self, *criteria, operator='AND', **kwargs):
        self.criteria_list = criteria
        self.operator = operator

    def toURLParams(self):
        fields = (' '+self.operator+' ').join([ ct.toURLParams() for ct in self.criteria_list ])
        return 'periode(%s)' % fields

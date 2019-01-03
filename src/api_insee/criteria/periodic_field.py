from .field import Field

class PeriodicField(Field):

    @property
    def representation(self):
        rp = super(PeriodicField, self).representation
        return 'periode(%s)' % rp

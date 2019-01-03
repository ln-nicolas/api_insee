

class ParamsExeption(Exception):

    name  = None
    value = None

    def __init__(self, name, value):
        self.name  = name
        self.value = value

    def wrongFormat(self, paramFormat):
        self.message = "Wrong format for %s : %s." % (self.name, self.value)
        self.message += "Exepted format %s " % (paramFormat)
        return self

    def __str__(self):
        return self.message

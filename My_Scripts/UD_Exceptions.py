""" User Defined Exceptions """


class ParameterOutOfBounds(Exception):

    def __init__(self, parameter):
        msg = f"Parameter is out of bounds, {parameter}"
        super(ParameterOutOfBounds, self).__init__(msg)
        self.parameter = parameter

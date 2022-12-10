

class Policy():

    """ Behaviour of an entity.
    A policy choses an action in a given state. """

    def __init__(self):
        pass# TODO


    def act(self, state):
        pass # TODO


    def __call__(self, *args, **kwargs):
        return self.act(*args, **kwargs)


    @classmethod
    def sample(cls):
        return cls() # TODO

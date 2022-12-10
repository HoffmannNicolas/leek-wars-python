

class Action():

    """ Atomic action an entity can do.
    There are a total of [5 + #weapons + #items x #cells] possible actions :
    - Move Up/Right/Down/Left (4)
    - End Turn (1)
    - Equip a weapon (#weapon)
    - Use any item on any cell (#items x #cells)
    """

    def __init__(self):
        pass # TODO

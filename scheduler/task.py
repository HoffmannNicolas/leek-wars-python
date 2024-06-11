

class Task():

    def __init__(self, raw_period=42):

        self.raw_period = raw_period
        self.next_run = None


    def get_interval(self):
        return self.raw_period
    

    def run(self):
        print(f"Task running at {self.get_interval()} !")



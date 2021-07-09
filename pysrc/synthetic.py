class SyntheticControl:
    def __init__(self,operation):
        self.operation = operation

    def call(self,synthetic_name):
        source = self.operation["plugin"]["synthetic"][synthetic_name].main() #source, additions
        #return source
class SyntheticControl:
    def __init__(self,operation):
        self.operation = operation

    def call(self,synthetic_name,base,add):
        source = self.operation["plugin"]["synthetic"][synthetic_name].main(base,add) #source, additions
        return source
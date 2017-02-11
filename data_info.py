#
# Just a container/struct to hold all params for data
# like data status, update etc.

class DataInfo:

    def __init__(self, progress, update, accconst, useconst):
        self.progress = progress
        self.update = update
        self.accconst = accconst
        self.useconst = useconst

    def show(self):
        print("----------[ Data Info ]---------------") 
        print("Progress . . : %s" % self.progress)
        print("Update . . . : %s" % self.update)
        print("Acc. const . : %s" % self.accconst)
        print("Use. const . : %s" % self.useconst)
        print("--------------------------------------") 

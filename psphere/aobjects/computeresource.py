from psphere import managedobjects
from psphere.network import utils
 
class ComputeResource(managedobjects.ComputeResource):
    def __init__(self, mo_ref, client):
        managedobjects.ComputeResource.__init__(self, mo_ref, client)

""" Begin Testing """        
def computeresource_test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    computeresource()
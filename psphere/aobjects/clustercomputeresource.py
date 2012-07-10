from psphere import managedobjects
from psphere.network import utils
from psphere.errors import TaskFailedError

class ClusterComputeResource(managedobjects.ClusterComputeResource):
    def __init__(self, mo_ref, client):
        managedobjects.ClusterComputeResource.__init__(self, mo_ref, client)
        self.vlans = {}
        self.client = client

    def __calc_free_mem(self, host_moref):
        """
        Calculate the available free memory on a host
        
        :param host_moref: managed object reference to a host
        :type host_moref: obj
        """
        try:
            totalMemMb = host_moref.summary.hardware.memorySize /1024 /1024
            usedMemMb = host_moref.summary.quickStats.overallMemoryUsage
            availableMemMb = totalMemMb - usedMemMb
            return availableMemMb
        except:
            """ We probably have a bad host in the cluster, lets skip it"""
            return 0
        
    def add_vlan(self, vlan, cidr):
        """
        Add a vlan and network to cluster
        
        :param vlan: a vlan ID. e.g. 209
        :type vlan: int
        :param cidr: Network in CIDR. e.g. 192.168.1.0/24
        :type cidr: str
        """
        self.vlans[vlan] = utils.Vlan(vlan, cidr)
        return self.vlans[vlan]
        
    @property
    def list_vlans(self):
        """
        List all the vlans in the cluster
        """
        return self.vlans.keys()
                
    def cluster_has_ip(self, ip):
        """
        Check if the cluster contains given IP
        
        :param ip: IP address to check. e.g. 192.168.1.15
        :type ip: str
        """
        for vlan in self.vlans.keys():
            if self.vlans[vlan].contains(ip):
                return True
        return False
        
    def vlan_containing(self, ip):
        """
        Return the vlan that contains the given IP
        
        :param ip: IP Address to check. e.g. 192.168.1.15
        :type ip: str
        """
        for vlan in self.vlans.keys():
            if self.vlans[vlan].contains(ip):
                return vlan
        return 1
        
    @property
    def best_host(self):
        """
        Return a managed object reference to the best host in the cluster
        based on the amount of free available memory since monster vms
        are monster memory hogs
        """
        hosts_list = {}
        for host in self.host:
            hosts_list[host] = self.__calc_free_mem(host)
        choice = max(hosts_list, key=hosts_list.get)
        return choice
    
    @property
    def nfs_datastores(self):
        """
        Return a list of managed object references to NFS datastores
        """
        nfs_stores = []
        for store in self.datastore:
            if store.summary.type == "NFS":
                nfs_stores.append(store)
        return nfs_stores
        
    @property
    def best_datastore(self):
        """
        Return a managed object reference to the best datastore in the cluster
        based on the amount of free space available on the datastore
        """
        datastores = {}
        
        for store in self.datastore:
            if store.summary.multipleHostAccess:
                datastores[store] = [store.summary.freeSpace, store]
                
        new_stores = \
            dict(map(lambda item: (item[1][0], item[0]), datastores.items()))

        best_store = new_stores[max(new_stores.keys())]
        return best_store


    @property
    def vms(self):
        """
        return a list of VM's within in the cluster
        """
        vms = []
        
        hosts = self.host
        
        if len(hosts) > 0:
            for host in hosts:
                for vm in host.vm:
                    vms.append(vm)
            return vms

    def _add_host(self, hostname=None, username=None, password=None, 
                        sslThumbprint=None, force_connect=False,):
        """
        Internal helper to add a host to a cluster.
        """
        host_spec = self.client.create("HostConnectSpec")
        host_spec.force = force_connect
        host_spec.hostName = hostname
        host_spec.userName = username
        host_spec.password = password
        host_spec.sslThumbprint = sslThumbprint

        # Since we aren't including a folder, delete it
        delattr(host_spec, "vmFolder")

        return self.AddHost_Task(spec=host_spec, asConnected=True)


    def add_host(self, async=True, hostname=None, username=None, password=None, 
                            sslThumbprint=None, force_connect=False,):
        """
        Add a physical host to the cluster

        :param async: Wait for the task to complete
        :type async: bool
        :param hostname: Hostname of the host being added
        :type hostname: str
        :param userame: Username to connect to the host. Usually root
        :type username: str
        :param password: Password to use to connect to the host.
        :type password: str
        :param force_connect: Even if connection fails, add the host
        :type force_connect: bool
        :param insecure: Ignore SSL thumbprint on host verification
        :type insecure: bool
        """

        try:
            task = self._add_host(hostname, username, password, \
                                    sslThumbprint, force_connect)

            if async:
                status = task.wait_for_state([task.STATE_SUCCESS,
                                                task.STATE_ERROR])

                if status == task.STATE_ERROR:
                    # Lets check for invalid thumbprints
                    if hasattr(task.info.error.fault, "selfSigned"):
                        sslThumbprint = task.info.error.fault.thumbprint
                        task = self._add_host(hostname, username, password, \
                                                sslThumbprint, force_connect)

                        # Wait for the task to complete
                        task.wait_for_state([task.STATE_SUCCESS])
                    else:
                        raise TaskFailedError(task.get_error_message)


                # return the host that was added
                return task.info.result

            return task

        except TaskFailedError, e:
            return e


def best_cluster(ccr_list):
    """
    Takes a list of ClusterComputeResources
    ccr_list = omoto.vmware.cluster.ComputeResource.all(client)
    and will calculate the best cluster to use in the list 
    based on memory
    """
    all_clusters = {}
    for ccr in ccr_list:
        all_clusters[ccr] = ccr.summary.effectiveMemory
    choice = max(all_clusters, key=all_clusters.get)
    return choice


""" Begin Testing """        
def clustercomputeresource_test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    clustercomputeresource()

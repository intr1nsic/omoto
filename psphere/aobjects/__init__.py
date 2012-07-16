from psphere.managedobjects import *

# Subclass managed objects that we have added additional
# functionality to

from psphere.aobjects.computeresource import ComputeResource
from psphere.aobjects.clustercomputeresource import ClusterComputeResource
from psphere.aobjects.datacenter import Datacenter
from psphere.aobjects.datastore import Datastore
from psphere.aobjects.task import Task
from psphere.aobjects.virtualmachine import VirtualMachine
from psphere.aobjects.hostsystem import HostSystem

classmap = dict((x.__name__, x) for x in (
    ExtensibleManagedObject,
    Alarm,
    AlarmManager,
    AuthorizationManager,
    ManagedEntity,
    ComputeResource,
    ClusterComputeResource,
    Profile,
    ClusterProfile,
    ProfileManager,
    ClusterProfileManager,
    View,
    ManagedObjectView,
    ContainerView,
    CustomFieldsManager,
    CustomizationSpecManager,
    Datacenter,
    Datastore,
    DiagnosticManager,
    Network,
    DistributedVirtualPortgroup,
    DistributedVirtualSwitch,
    DistributedVirtualSwitchManager,
    EnvironmentBrowser,
    HistoryCollector,
    EventHistoryCollector,
    EventManager,
    ExtensionManager,
    FileManager,
    Folder,
    GuestAuthManager,
    GuestFileManager,
    GuestOperationsManager,
    GuestProcessManager,
    HostAuthenticationStore,
    HostDirectoryStore,
    HostActiveDirectoryAuthentication,
    HostAuthenticationManager,
    HostAutoStartManager,
    HostBootDeviceSystem,
    HostCacheConfigurationManager,
    HostCpuSchedulerSystem,
    HostDatastoreBrowser,
    HostDatastoreSystem,
    HostDateTimeSystem,
    HostDiagnosticSystem,
    HostEsxAgentHostManager,
    HostFirewallSystem,
    HostFirmwareSystem,
    HostHealthStatusSystem,
    HostImageConfigManager,
    HostKernelModuleSystem,
    HostLocalAccountManager,
    HostLocalAuthentication,
    HostMemorySystem,
    HostNetworkSystem,
    HostPatchManager,
    HostPciPassthruSystem,
    HostPowerSystem,
    HostProfile,
    HostProfileManager,
    HostServiceSystem,
    HostSnmpSystem,
    HostStorageSystem,
    HostSystem,
    HostVirtualNicManager,
    HostVMotionSystem,
    HttpNfcLease,
    InventoryView,
    IpPoolManager,
    IscsiManager,
    LicenseAssignmentManager,
    LicenseManager,
    ListView,
    LocalizationManager,
    OptionManager,
    OvfManager,
    PerformanceManager,
    ProfileComplianceManager,
    PropertyCollector,
    PropertyFilter,
    ResourcePlanningManager,
    ResourcePool,
    ScheduledTask,
    ScheduledTaskManager,
    SearchIndex,
    ServiceInstance,
    SessionManager,
    StoragePod,
    StorageResourceManager,
    Task,
    TaskHistoryCollector,
    TaskManager,
    UserDirectory,
    ViewManager,
    VirtualApp,
    VirtualDiskManager,
    VirtualizationManager,
    VirtualMachine,
    VirtualMachineCompatibilityChecker,
    VirtualMachineProvisioningChecker,
    VirtualMachineSnapshot,
    VmwareDistributedVirtualSwitch
))
def classmapper(name):
    return classmap[name]

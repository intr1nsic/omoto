.. highlight:: python

An introduction to psphere
==========================

This document will provide an introduction to psphere fundamentals and a brief
background of the `vSphere Web Services SDK`_.


vSphere Web Services SDK
------------------------

While you can get started performing rudimentary operations using only this
documentation, working knowledge of the `vSphere Web Services SDK`_ and the
terminology used will accelerate your learning.

As you perform more complicated operations you will definitely be consulting
the vendor documentation.

I recommend the following guides (which I can only reference by title due to
the VMware documentation layout):

* vSphere Web Services SDK Programming Guide
* VMware vSphere API Reference

Throughout this documentation there are links to the vendor documentation where
appropriate.


The Client object
-----------------

Like many Python libraries, the Client object is the entry point into the
remote service.

Instantiating a Client object will log into the remote service
and allow you to obtain Python objects representing managed objects. You can
then access information and execute methods using those objects.


Hello World in psphere
----------------------

Not quite, but logging into the server and printing the current time is close::

    >>> from psphere.client import Client
    >>> client = Client("your.esxserver.com", "Administrator", "strongpass")
    >>> servertime = client.si.CurrentTime()
    >>> print(servertime)
    2010-09-04 18:35:12.062575
    >>> client.logout()


General programming pattern
---------------------------

Create a new Client::

    >>> from psphere.client import Client
    >>> client = Client("your.esxserver.com", "Administrator", "strongpass")

...if we inspect the rootFolder attribute of the client's content attribute
we can see it's a Python object::

    >>> root_folder = client.si.content.rootFolder
    >>> root_folder.__class__
    <class 'psphere.managedobjects.Folder'>

...we can then access properties of it::

    >>> print(root_folder.name)
    Datacenters

...and invoke a method on it::

    >>> new_folder = root_folder.CreateFolder(name="New")
    >>> print(new_folder.name)
    New
    >>> task = new_folder.Destroy_Task()
    >>> print(task.info.state)
    success

...finally, we log out of the server::

    >>> client.logout()


.. |more| image:: more.png
          :align: middle
          :alt: more info    

.. _VMware vSphere Web Services SDK: http://pubs.vmware.com/vsphere-50/index.jsp?topic=/com.vmware.wssdk.apiref.doc_50/right-pane.html

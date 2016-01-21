#!/bin/env python

'''
The goal of this project is to supply a reusable config
library, that can expand to cope with distributed and remote config

The intention with holodeck is to build a set of compents that allow
me to build, wrap and deploy python packages in LXC containers or in just venvs with minimum fuss

As such we are expecting to pass around and promote immutable 'containers' (lxc or venvs) and will need ways for these to pick themselves 
up and configure themselves

Global config naming convention
-------------------------------

All names will have the pypi package namespace as the top level.::

    pyholodeck

Then each package can define its own, unique within the packge set of 
variables::

    pyholodeck.listen.port
    pyholodeck.foo.bar

Every config item will always be storeable as a text file in the .ini format, and will be held in process as a plain python dict.

I will not at all support other formatsm the temptation to put executable code in config should be resisted at all costs.



'''
import os
import logging
from ConfigParser import SafeConfigParser


def configme(pkg_name):
    '''Given a pkg name, can I get the two possible locations to 
       gather config
    '''
    confd = {}
    well_known_dir = os.path.join('/usr/local/etc/', pkg_name)
    well_known_location = os.path.join(well_known_dir, 'conf.ini')
    confp = SafeConfigParser()
    try:
        confp.read(well_known_location)
    except:
        #: no config at all ????
        #: need a default
        return confd
    
    for section in confp.sections():
        #[IAmASection]
        print section
        if section not in confd:
            confd[section] = {}
        options = confp.options(section)
        for option in options:
            try:
                print option
                print confp.get(section, option)
                confd[section][option] = confp.get(section, option)
            except Exception, e:
                
                logging.error("Failed to add config to confd %s %s %s", e, section, option)
    return confd



from jjsystem.common import subsystem
from jjlocal.subsystem.sysadmin.ibge_sync import resource

from better_than_yesterday.subsystem.jjlocal.ibge_sync import manager

subsystem = subsystem.Subsystem(resource=resource.IbgeSync,
                                manager=manager.Manager)

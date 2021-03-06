__author__ = "Pranav Srinivas Kumar"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Pranav Srinivas Kumar"
__email__ = "pkumar@isis.vanderbilt.edu"
__status__ = "Production"

import os, sys, inspect

working_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(working_dir, "templates")
# Recursively compile on template files in templates directory
os.system("/usr/local/bin/cheetah compile " + template_dir + "/*.tmpl")
cfs_templates = os.path.realpath(os.path.abspath
                                 (os.path.join
                                  (os.path.split
                                   (inspect.getfile
                                    (inspect.currentframe()
                                 )
                                )[0], "templates")
                              ))
if cfs_templates not in sys.path:
    sys.path.insert(0, cfs_templates)
# From template import *    
from app_version import *
from app_events import *
from app_msg import *
from app_source import *
from app_header import *
from app_perfids import *
from app_msgids import *
from cpu1_Makefile import *
from cpu1_cfe_es_startup import *
from app_Makefile import *

class cFE_Application_Generator:
    def generate(self, mission):
        self.mission_home = mission.mission_home
        self.apps_dir = os.path.join(self.mission_home, 'apps')
        self.build_dir = os.path.join(self.mission_home, 'build')
        self.cpu1_dir = os.path.join(self.build_dir, 'cpu1')
        apps_list = []
        for app in mission.apps:
            apps_list.append(app.name)
        # Generate cpu1 Makefile
        makefile_namespace = {'apps' : apps_list}
        t = cpu1_Makefile(searchList=[makefile_namespace])
        self.cpu1_makefile = str(t)
        with open(os.path.join(self.cpu1_dir, 'Makefile'), 'w') as temp_file:
            temp_file.write(self.cpu1_makefile)

        # Generate cpu1 cfe_es_startup.scr
        cfe_es_startup_namespace = {'apps' : apps_list}
        t = cpu1_cfe_es_startup(searchList=[cfe_es_startup_namespace])
        self.cpu1_cfe_es_startup = str(t)
        self.cpu1_exe = os.path.join(self.cpu1_dir, 'exe')
        with open(os.path.join(self.cpu1_exe, 'cfe_es_startup.scr'), 'w') as temp_file:
            temp_file.write(self.cpu1_cfe_es_startup)

        for app in mission.apps:
            app_makefile_dir = os.path.join(self.cpu1_dir, app.name)
            if not os.path.exists(app_makefile_dir):
                os.makedirs(app_makefile_dir)
            app_makefile_namespace = {'application_name' : app.name, 
                                      'application_name_caps' : app.name.upper()}
            t = app_Makefile(searchList=[app_makefile_namespace])
            self.app_makefile = str(t)
            with open(os.path.join(app_makefile_dir, "Makefile"), 'w') as temp_file:
                temp_file.write(self.app_makefile)
        
        for app in mission.apps:
            app_home = os.path.join(self.apps_dir, app.name)
            if not os.path.exists(app_home):
                os.makedirs(app_home)
            app_fsw = os.path.join(app_home, 'fsw')
            app_docs = os.path.join(app_home, 'docs')
            app_tg = os.path.join(app_home, 'test and ground')
            if not os.path.exists(app_fsw):
                os.makedirs(app_fsw)
            if not os.path.exists(app_docs):
                os.makedirs(app_docs)
            if not os.path.exists(app_tg):
                os.makedirs(app_tg)
            fsw_build = os.path.join(app_fsw, 'for_build')
            fsw_src = os.path.join(app_fsw, 'src')
            fsw_tables = os.path.join(app_fsw, 'tables')
            fsw_mission_inc = os.path.join(app_fsw, 'mission_inc')
            fsw_platform_inc = os.path.join(app_fsw, 'platform_inc')
            fsw_ut = os.path.join(app_fsw, 'unit_test')
            if not os.path.exists(fsw_build):
                os.makedirs(fsw_build)
            if not os.path.exists(fsw_src):
                os.makedirs(fsw_src)
            if not os.path.exists(fsw_tables):
                os.makedirs(fsw_tables)
            if not os.path.exists(fsw_mission_inc):
                os.makedirs(fsw_mission_inc)
            if not os.path.exists(fsw_platform_inc):
                os.makedirs(fsw_platform_inc)
            if not os.path.exists(fsw_ut):
                os.makedirs(fsw_ut)

            ###
            ## Generating App Version Header File
            ###
            version_file = app.name + '_version.h'
            version_length = 0
            for key, value in app.version.items():
                if len(key) > version_length:
                    version_length = len(key)
            for key, value in app.version.items():
                space = '    '
                for i in range(0, version_length - len(key)):
                    space += ' '
                app.version[key + space] = app.version[key]
                del app.version[key]
            version_list = []
            for key, value in app.version.items():
                version_list.append(key + value)
            version_namespace = {'application_name' : app.name,
                                 'dollar_id' : '$Id',
                                 'version' : app.version,
                                 'version_list' : version_list}
            t = app_version(searchList=[version_namespace])
            self.version = str(t)
            with open(os.path.join(fsw_src, version_file), 'w') as temp_file:
                temp_file.write(self.version)

            ###
            ## Generating App Performance IDs Header File
            ###
            perfids_file = app.name + '_perfids.h'
            perfids_length = 0
            for key, value in app.perf_ids.items():
                if len(key) > perfids_length:
                    perfids_length = len(key)
            for key, value in app.perf_ids.items():
                space = '    '
                for i in range(0, perfids_length - len(key)):
                    space += ' '
                app.perf_ids[key + space] = app.perf_ids[key]
                del app.perf_ids[key]
            perf_ids_list = []
            for key, value in app.perf_ids.items():
                perf_ids_list.append(key+value)
            perf_namespace = {'application_name' : app.name,
                              'perf_ids' : app.perf_ids,
                              'dollar_id' : '$Id',
                              'perf_ids_list' : perf_ids_list}
            t = app_perfids(searchList=[perf_namespace])
            self.perfids = str(t)
            with open(os.path.join(fsw_mission_inc, perfids_file), 'w') as temp_file:
                temp_file.write(self.perfids)

            ###
            ## Generating App Message IDs Header File
            ###%
            msgids_file = app.name + '_msgids.h'
            msgids_length = 0
            for key, value in app.msg_ids.items():
                if len(key) > msgids_length:
                    msgids_length = len(key)
            for key, value in app.msg_ids.items():
                space = '    '
                for i in range(0, msgids_length - len(key)):
                    space += ' '
                app.msg_ids[key + space] = app.msg_ids[key]
                del app.msg_ids[key]
            msg_ids_list = []
            for key, value in app.msg_ids.items():
                msg_ids_list.append(key+value)
            msg_namespace = {'application_name' : app.name,
                             'msg_ids' : app.msg_ids,
                             'dollar_id' : '$Id',
                             'msg_ids_list' : msg_ids_list}
            t = app_msgids(searchList=[msg_namespace])
            self.msgids = str(t)
            with open(os.path.join(fsw_platform_inc, msgids_file), 'w') as temp_file:
                temp_file.write(self.msgids)

            ###
            ## Generating App Events Header File
            ###
            events_file = app.name + '_events.h'
            event_length = 0
            for key, value in app.event_ids.items():
                if len(key) > event_length:
                    event_length = len(key)
            for key, value in app.event_ids.items():
                space = '    '
                for i in range(0, event_length - len(key)):
                    space += ' '
                app.event_ids[key + space] = app.event_ids[key]
                del app.event_ids[key]
            event_ids_list = []
            for key, value in app.event_ids.items():
                event_ids_list.append(key+value)
            event_namespace = {'application_name' : app.name,
                               'event_ids' : app.event_ids,
                               'event_ids_list' : event_ids_list}
            t = app_events(searchList=[event_namespace])
            self.events = str(t)
            with open(os.path.join(fsw_src, events_file), 'w') as temp_file:
                temp_file.write(self.events)

            ###
            ## Generating App Msg Header File
            ###
            msg_file = app.name + '_msg.h'

            # Neatly Format Command Codes
            cmd_length = 0
            for key, value in app.command_codes.items():
                if len(key) > cmd_length:
                    cmd_length = len(key)
            for key, value in app.command_codes.items():
                space = '    '
                for i in range(0, cmd_length - len(key)):
                    space += ' '
                app.command_codes[key + space] = app.command_codes[key]
                del app.command_codes[key]

            for msg in app.messages:
                field_length = 0
                for field in msg.fields:
                    if len(field[0]) > field_length:
                        field_length = len(field[0])
                for i in range(0, len(msg.fields)):
                    space = '            '
                    for i in range(0, field_length - len((msg.fields[i])[0])):
                        space += ' '
                    msg.fields[i] = [(msg.fields[i])[0] + space, (msg.fields[i])[1]]

            msg_namespace = {'application_name' : app.name,
                             'command_codes' : app.command_codes,
                             'command_codes_dict' : app.command_codes.items(),
                             'messages': app.messages}
            t = app_msg(searchList=[msg_namespace])
            self.msg = str(t)
            with open(os.path.join(fsw_src, msg_file), 'w') as temp_file:
                temp_file.write(self.msg)
               
            ###
            ## Generating App Source File
            ###
            msgids_list = []
            for key, value in app.msg_ids.items():
                msgids_list.append(key)
            cc_list = []
            for key, value in app.command_codes.items():
                cc_list.append(key)
            app_name_caps = app.name.upper()
            c_file = app.name + '.c'
            c_namespace = {'application_name' : app.name,
                           'application_name_caps' : app_name_caps,
                           'msgids' : msgids_list, 
                           'cmdcodes' : cc_list}
            t = app_source(searchList=[c_namespace])
            self.c = str(t)
            with open(os.path.join(fsw_src, c_file), 'w') as temp_file:
                temp_file.write(self.c)

            ###
            ## Generating App Header File
            ###
            h_file = app.name + '.h'
            h_namespace = {'application_name' : app.name,
                           'application_name_caps' : app_name_caps}
            t = app_header(searchList=[h_namespace])
            self.h = str(t)
            with open(os.path.join(fsw_src, h_file), 'w') as temp_file:
                temp_file.write(self.h)
                

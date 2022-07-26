#!/usr/bin/env python

import os
import sys
import requests
from shutil import copyfile
from .workspaceClient import Workspace
from .AbstractHandleClient import AbstractHandle

def link_or_copy(src, dst):
    try:
        os.link(src, dst)
    except OSError:
        print("Falling back to copy")
        copyfile(src, dst)


class WSUtils():
    def __init__(self):
        ws_url = os.environ["WS_URL"]
        hs_url = os.environ["HS_URL"]
        self.token = os.environ["WORKSPACE_TOKEN"]
        self.ws = Workspace(ws_url, token=self.token)
        self.hs = AbstractHandle(hs_url, token=self.token)
        self.debug = False

    def _debug(self, mess):
        if self.debug:
            print(mess)

    def handle_to_file(self, hid, f_name):
        handle = self.hs.hids_to_handles([hid])[0]
        h = {'Authorization': 'Oauth {}'.format(self.token)}
        data = requests.get('{url}/node/{id}?download'.format(**handle), headers=h)
        with open(f_name, "w") as f:
            f.write(data.text)

    def ws_get(self, upa, include=None):
        """
        Wrapper around get_objects

        TODO: Make this work for admin and non-admin
        """
        p = {'objects': [{'ref': upa}]}
        if include:
            p = {'objects': [{'ref': upa, 'included': include}]}
        resp = self.ws.administer({'command': 'getObjects', 'params': p})
        return resp

    def list_workspaces(self, public=False):
        """
        list workspaces.  If public is set then just public workspaces.
        """
        if public:
            return self.ws.list_workspace_ids({'onlyGlobal': 1})['pub']
        else:
            raise OSError("NotImplemented")

    def list_objects(self, wsid, filter=None):
        """
        list objects
        """
        offset = 0
        results = 1
        batchsize = 10000
        f_objs = []
        while results < batchsize and results > 0:
            p = {'ids': [wsid], 
                 'minObjectID': offset+1,
                 'maxObjectID': offset+batchsize}
            objs = self.ws.administer({'command': 'listObjects', 'params': p})
            results = len(objs)
            for obj in objs:
                if filter:
                    if obj[2].startswith(filter):
                        f_objs.append(obj)
                else:
                    f_objs.append(obj)
            offset += batchsize
        return f_objs

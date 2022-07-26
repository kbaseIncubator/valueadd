#!/usr/bin/env python

import os
import sys
import requests
from shutil import copyfile
from utils.workspaceClient import Workspace
from utils.AbstractHandleClient import AbstractHandle

def link_or_copy(src, dst):
    try:
        os.link(src, dst)
    except OSError:
        print("Falling back to copy")
        copyfile(src, dst)



class Prestage():
    def __init__(self):
        ws_url = os.environ["WS_URL"]
        hs_url = os.environ["HS_URL"]
        self.token = os.environ["WORKSPACE_TOKEN"]
        self.ws = Workspace(ws_url, token=self.token)
        self.hs = AbstractHandle(hs_url, token=self.token)
        self.cache_dir = os.environ.get('CACHE_DIR')
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

    def fetch_genome_assembly(self, upa, f_name):
        """
        routine to handle getting the fasta from an assembly object
        """
        resp = self.ws_get(upa, ['fasta_handle_info', 'fasta_handle_ref', 'assembly_ref'])
        data = resp['data'][0]['data']
        if 'fasta_handle_info' in data:
            hid = data['fasta_handle_info']['handle']['hid']
        elif 'fasta_handle_ref' in data:
            hid = data['fasta_handle_ref']
        elif 'assembly_ref' in data:
            # Fetch the assembly ref data
            self.fetch_genome_assembly(data['assembly_ref'], f_name)
            return
        else:
            raise ValueError("No handle")
        self.handle_to_file(hid, f_name)

    def cacher(self, typ, upa):
        """
        Cacher routine that will call the right special
        routine.  If cache_dir is set then the object will
        be read/written to the cache area.

        TODO: Make the hard link work better
        """
        if typ == "assembly":
            f_name = "{}_assembly.fna".format(upa.replace('/', '_'))
            fetcher = self.fetch_genome_assembly
        else:
            raise ValueError("Not yet supported")
        wsid = upa.split('/')[0]
        cache_file = None
        if self.cache_dir:
            cache_file = '{}/{}/{}'.format(self.cache_dir, wsid, f_name)
        if os.path.exists(f_name):
            self._debug("already fetched")
            sys.exit()
        elif cache_file and os.path.exists(cache_file):
            self._debug("linking")
            link_or_copy(cache_file, f_name)
        else:
            self._debug("fetching")
            fetcher(upa, f_name)
            if cache_file:
                self._debug("caching")
                ddir = '{}/{}'.format(self.cache_dir, wsid)
                if not os.path.exists(ddir):
                    os.makedirs(ddir)
                link_or_copy(f_name, cache_file)


if __name__ == "__main__":
    typ = sys.argv[1]
    ps = Prestage()
    for upa in sys.argv[2:]:
        ps.cacher(typ, upa)

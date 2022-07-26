import requests
import os
import sys
import json
import tempfile


def _json_tmp(data):
    fp, fname = tempfile.mkstemp(suffix='.json')
    with os.fdopen(fp, 'w') as fd:
        fd.write(json.dumps(data))
    return fname


class Cromwell():
    def __init__(self):
        self.url = os.environ.get("CROMWELL_URL").rstrip("/")

    def submit(self, wdl, inputs, options=None, dryrun=False, verbose=False):
        """
        Submit a job
        """

        infname = _json_tmp(inputs)
        bundle = "bundle.zip"

        # Write input file
        files = {
            'workflowSource': open(wdl),
            'workflowInputs': open(infname),
            'workflowDependencies': open(bundle, 'rb')
        }

        # TODO: Add something to handle priority
        #if options:
        #    files['workflowOptions'] = open(options)

        if not dryrun:
            url = "%s/api/workflows/v1" % (self.url)
            resp = requests.post(url, data={}, files=files)
            print(resp.text)
            job_id = json.loads(resp.text)['id']
        else:
            job_id = "dryrun"
        for fld in files:
            files[fld].close()

        os.unlink(infname)
        #if labels:
        #    os.unlink(lblname)

        return job_id

    def meta(self, job):
        url = "%s/api/workflows/v1/%s/metadata" % (self.url, job)
        resp = requests.get(url)
        return resp.json()

    def query(self, state=None, filter=None):
        url = "%s/api/workflows/v1/query" % (self.url)
        if state:
            url += '?status=%s' % (state)
        resp = requests.get(url)
        return resp.json()


if __name__ == "__main__":

    crom = Cromwell()
    if sys.argv[1] == "submit":
        wdl = sys.argv[2]
        inp = sys.argv[3]
        inpd = json.load(open(inp))
        crom.submit(wdl, inpd)
    elif sys.argv[1] == "meta":
        job = sys.argv[2]
        meta = crom.meta(job)
        print(json.dumps(meta, indent=2))

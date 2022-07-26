from .cromwell import Cromwell

#  execution:
#    type: wdl
#    wdl: gtdbtk.wdl
#    input_params:
#      fasta: "{{ assembly }}"
#      "gtdbtk_re.fasta": "{{ assembly }}"
#      "gtdbtk_re.upa": "{{ upa }}"
#    prestage:
#    - assembly
#    refdata:
#    - /kbase/cache/gtdbtk/release207_v2:/refdata


def run_wdl(pipeline, event):
    execution = pipeline["execution"]
    params = {
      "upa": event.upa,
    }
    wdl = "./wdls/" + execution["wdl"]
    inputs = dict()
    for k, v in execution["input_params"].items():
        print(k, v)
        inputs[k] = v.format(**params)
    print(inputs)
    print(event)
    print(pipeline)
    crom = Cromwell()
    crom.submit(wdl, inputs)




def run_pipeline(pipeline, event):
    execution = pipeline["execution"]
    if execution["type"].lower() == "wdl":
        run_wdl(pipeline, event)

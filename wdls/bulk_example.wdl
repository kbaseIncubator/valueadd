
version 1.0

import "utils.wdl" as utils


workflow bulkex {
    input {
        String filter="KBaseGenomeAnnotations.Assembly"
    }

    call utils.get_workspaces as gws
    scatter (wsid in gws.wsids) {
        call fetch_data as fd { input: wsid=wsid, filter=filter }
    }
    
    meta {
        author: "Shane Canon"
        email: "scanon@lbl.gov"
        description: "Example of Bulk Analysis"
        version: "1.0.0"
    }
}

task fetch_data {
    input {
        String wsid
        String filter
        String svc_url="https://ci.kbase.us/services"
        String dollar="$"
    }

    command <<<
        export WS_URL=~{svc_url}/ws
        export HS_URL=~{svc_url}/handleservice
        export WORKSPACE_TOKEN=$(cat /secrets/token)
        export CACHE_DIR=/cache

        python /src/ws.py list_objects ~{wsid} ~{filter}| head -1| \
               grep -v -- 1.0| \
               awk '{print "~{wsid}/"$1"/"$5}' | \
               xargs python /src/prestage.py assembly

    >>>

    output {
    }

    runtime {
        docker: "docker.io/scanon/prestage:dev"
        memory: "2 GB"
        cpu: 1
    }
}



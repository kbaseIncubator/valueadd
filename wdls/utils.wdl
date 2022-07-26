version 1.0

task get_workspaces {
    input {
        String svc_url="https://ci.kbase.us/services"
    }

    command {
        export WS_URL=~{svc_url}/ws
        export HS_URL=~{svc_url}/handleservice
        export WORKSPACE_TOKEN=$(cat /secrets/token)

        python /src/ws.py list_public
    }

    output {
        Array[String] wsids = read_lines(stdout())
    }

    meta {
        volatile: true
    }

    runtime {
        docker: "docker.io/scanon/prestage:dev"
        memory: "2 GB"
        cpu: 1
    }
}

task list_objects {
    input {
        String wsid
        String filter
        String svc_url="https://ci.kbase.us/services"
    }

    command {
        export WS_URL=~{svc_url}/ws
        export HS_URL=~{svc_url}/handleservice
        export WORKSPACE_TOKEN=$(cat /secrets/token)

        python /src/ws.py list_objects ~{wsid} ~{filter} 
    }

    output {
    }

    meta {
        volatile: true
    }

    runtime {
        docker: "docker.io/scanon/prestage:dev"
        memory: "2 GB"
        cpu: 1
    }
}

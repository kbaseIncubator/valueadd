version 1.0

task stage_assembly {

    input {
        String upa
        String svc_url="https://ci.kbase.us/services"
    }

    command <<<
        export WS_URL=~{svc_url}/ws
        export HS_URL=~{svc_url}/handleservice
        export CACHE_DIR=/cache
        export WORKSPACE_TOKEN=$(cat /secrets/token)
        python /src/prestage.py assembly ~{upa}
    >>> 

    output {
        File assembly = glob("*.fna")[0]
    }

    runtime {
        docker: "docker.io/scanon/prestage:dev"
        memory: "1 GB"
    }
}


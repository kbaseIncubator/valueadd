
version 1.0

import "stage.wdl" as stage
 

workflow gtdbtk2re {
    input {
        String upa
    }

    call stage.stage_assembly as stg { input: upa=upa }
    call gtdbtk { input: fasta_input=stg.assembly }

    meta {
        author: "Shane Canon"
        email: "scanon@lbl.gov"
        description: "Run GTDBtk on an input genome"
        version: "2.1.1"
    }
}

task gtdbtk {
    input {
        File fasta_input
    }

    command {
        # gtdbtk doesn't like the raw filename in inputs
        ln -s ~{fasta_input} input.fna
       
        # gtdbtk doesn't like using the default tmp from Cromwell 
        export TMPDIR=/tmp
        gtdbtk classify_wf --genome_dir . --out out --cpus 8
    }

    output {
        File gtdbtk_summary = glob("out/gtdbtk.*.summary.tsv")[0]
        File gtdbtk_log = "out/gtdbtk.log"
    }

    runtime {
        docker: "docker.io/ecogenomic/gtdbtk:2.1.1"
        memory: "128 GB"
        cpu: 8
        database: "gtdbtk/release207_v2/:/refdata"
    }
}


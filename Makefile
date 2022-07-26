IMAGE="scanon/prestage:dev"

submits:
	python ./src/utils/cromwell.py submit ./wdls/stage.wdl tests/input2.json

submitg:
	python ./src/utils/cromwell.py submit ./wdls/gtdb.wdl tests/input.json

validate:
	java -jar ~/womtool-57.jar validate ./wdls/gtdb.wdl

image:
	docker build -t $(IMAGE) -f Dockerfile.staging .
	docker push $(IMAGE)

bundle:
	cd wdls && zip ../bundle.zip *wdl

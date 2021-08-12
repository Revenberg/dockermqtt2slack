# dockerwatermeter

sudo apt install gnupg2 pass
docker image build -t dockerwatermeter  .
docker login -u revenberg
docker image push revenberg/dockerwatermeter:latest

docker run revenberg/dockerwatermeter

docker exec -it ??? /bin/sh

docker push revenberg/dockerwatermeter:
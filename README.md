# dockermqtt2slack

sudo apt install gnupg2 pass
docker image build -t dockermqtt2slack  .
docker login -u revenberg
docker image push revenberg/dockermqtt2slack:latest

docker run revenberg/dockermqtt2slack

docker exec -it ??? /bin/sh

docker push revenberg/dockermqtt2slack:
# dockermqtt2slack

sudo apt install gnupg2 pass
docker image build -t dockermqtt2slack:latest  .
docker login -u revenberg
docker image push revenberg/dockermqtt2slack:latest

docker run revenberg/dockermqtt2slack

docker exec -it ??? /bin/sh

docker push revenberg/dockermqtt2slack:latest

# ~/dockermqtt2slack/build.sh;docker rm -f $(docker ps | grep mqtt2slack | cut -d' ' -f1);cd /var/docker-compose;docker-compose up -d mqtt2slack;docker logs -f $(docker ps | grep mqtt2slack | cut -d' ' -f1)
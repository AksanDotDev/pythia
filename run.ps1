docker stop Pythia
docker rm Pythia
docker rmi pythia
docker build -t pythia .
docker run --net=host --restart=unless-stopped --name Pythia -v /d/pythia/__env__:/__env__ pythia
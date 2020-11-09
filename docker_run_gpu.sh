# Run container on GPU
docker run --net=host --gpus all -v $(pwd)/app:/app -d entro-jukebox_entro-jukebox:latest

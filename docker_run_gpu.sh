# Run Worker
docker run --net=host --gpus all -d entro-jukebox_entro-jukebox:latest

# Run FastAPI
docker run --net=host --gpus all --entrypoint "/venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8080 " -d entro-jukebox:latest
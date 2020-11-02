import app.jukebox
import torch as t
import librosa
import os
from IPython.display import Audio
from app.jukebox.make_models import make_vqvae, make_prior, MODELS, make_model
from app.jukebox.hparams import Hyperparams, setup_hparams
from app.jukebox.sample import sample_single_window, _sample, \
                           sample_partial_window, upsample
from app.jukebox.utils.dist_utils import setup_dist_from_mpi
from app.jukebox.utils.torch_utils import empty_cache
rank, local_rank, device = setup_dist_from_mpi()

def generate_audio(request):
    response = request
    return response
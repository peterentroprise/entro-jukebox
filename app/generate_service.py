import app.jukebox as jukebox
import torch as t
import librosa
import os
from app.models.common import GenerateRequest
from IPython.display import Audio
from app.jukebox.make_models import make_vqvae, make_prior, MODELS, make_model
from app.jukebox.hparams import Hyperparams, setup_hparams
from app.jukebox.sample import sample_single_window, _sample, \
                           sample_partial_window, upsample
from app.jukebox.utils.dist_utils import setup_dist_from_mpi
from app.jukebox.utils.torch_utils import empty_cache
rank, local_rank, device = setup_dist_from_mpi()


def generate_audio(request: GenerateRequest):
    model = request.model
    hps = Hyperparams()
    hps.sr = 44100
    hps.n_samples = 3 if model=='5b_lyrics' else 8
    hps.name = '/content/drive/My Drive/blink_182_punk'
    chunk_size = 16 if model=="5b_lyrics" else 32
    max_batch_size = 3 if model=="5b_lyrics" else 16
    hps.levels = 3
    hps.hop_fraction = [.5,.5,.125]

    vqvae, *priors = MODELS[model]
    vqvae = make_vqvae(setup_hparams(vqvae, dict(sample_length = 1048576)), device)
    top_prior = make_prior(setup_hparams(priors[-1], dict()), vqvae, device)


    response = request
    return response
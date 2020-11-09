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

def generate_audio_full(request: GenerateRequest):
    model = request.model
    hps = Hyperparams()
    hps.sr = 44100
    hps.n_samples = 1
    hps.name = '/sample'
    chunk_size = 8
    max_batch_size = 1
    hps.levels = 1
    hps.hop_fraction = [.5,.5,.125]

    vqvae, *priors = MODELS[model]
    vqvae = make_vqvae(setup_hparams(vqvae, dict(sample_length = 1048576)), device)
    top_prior = make_prior(setup_hparams(priors[-1], dict()), vqvae, device)

    sample_length_in_seconds = request.sample_length_in_seconds

    hps.sample_length = (int(sample_length_in_seconds*hps.sr)//top_prior.raw_to_tokens)*top_prior.raw_to_tokens
    assert hps.sample_length >= top_prior.n_ctx*top_prior.raw_to_tokens, f'Please choose a larger sampling rate'

    metas = [dict(artist = request.artist,
                genre = request.genre,
                total_length = hps.sample_length,
                offset = 0,
                lyrics = request.lyrics,
                ),
            ] * hps.n_samples
    labels = [None, None, top_prior.labeller.get_batch_labels(metas, 'cuda')]

    sampling_temperature = .98

    lower_batch_size = 16
    max_batch_size = 3 if model == "5b_lyrics" else 16
    lower_level_chunk_size = 32
    chunk_size = 16 if model == "5b_lyrics" else 32
    sampling_kwargs = [dict(temp=.99, fp16=True, max_batch_size=lower_batch_size,
                            chunk_size=lower_level_chunk_size),
                        dict(temp=0.99, fp16=True, max_batch_size=lower_batch_size,
                            chunk_size=lower_level_chunk_size),
                        dict(temp=sampling_temperature, fp16=True, 
                            max_batch_size=max_batch_size, chunk_size=chunk_size)]

    zs = [t.zeros(hps.n_samples,0,dtype=t.long, device='cuda') for _ in range(len(priors))]
    zs = _sample(zs, labels, sampling_kwargs, [None, None, top_prior], [2], hps)
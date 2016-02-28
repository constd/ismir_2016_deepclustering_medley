from multiprocessing import Pool
import medleydb as mdb
import librosa as lr
import pandas as pd
import numpy as np
import argparse
import scipy
import os


def get_audio(filename):
    audio, _ = lr.core.load(filename,
                            sr=44100,
                            mono=True)
    return audio


def get_spectrum(audio, complex=True):
    spec = lr.stft(audio,
                   n_fft=4096,
                   hop_length=256,
                   win_length=2048,
                   window=scipy.signal.blackmanharris)
    if not complex:
        return np.abs(spec)
    return spec


def get_mask(spectrum, threshold, binary=True):
    mask = np.array(20.*np.log10(spectrum) >= threshold,
                    dtype=np.int)
    if binary:
        return mask
    return mask * spectrum


def iter_stems(stemlist, outpath, t, instr_type):
    # t is the threshold for the mask
    # I'm exposing it so we can play with it
    for stem in stemlist:
        print 'Processing {}'.format(stem)
        audio = get_audio(stem)
        spectrum = get_spectrum(audio)
        mask = get_mask(spectrum, t)
        sbn = os.path.basename(stem)
        np.savez('{}{}_{}'.format(outpath, instr_type, sbn[:-4]),
                 spec=spectrum, mask=mask)


def parallel_iter_stem(x):
    stem, outpath, t, instr_type = x
    print 'Processing {}'.format(stem)
    audio = get_audio(stem)
    spectrum = get_spectrum(audio)
    mask = get_mask(spectrum, t)
    sbn = os.path.basename(stem)
    np.savez('{}{}_{}'.format(outpath, instr_type, sbn[:-4]),
             spec=spectrum, mask=mask)


def select_instrument(args, it):
    valid_instruments = mdb.get_valid_instrument_labels()
    if args.parallel == 'p':
        pool = Pool(8)
    # check if the given instrument exists
    if args.instrtype not in valid_instruments:
        raise 'Not a valid instrument. Valid instruments are: {}'.format(', '.join(valid_instruments))
    # get all available files (duh!) for the selected instrument
    instr_files = mdb.get_files_for_instrument(args.instrtype)
    if args.parallel == 'p':
        # wrap the input args to hackily parallelize the process
        pargs = [[x, args.outpath, args.t, it] for x in instr_files]
        pool.map(parallel_iter_stem, pargs)
    elif args.parallel == 's':
        iter_stems(instr_files, args.outpath, args.t, it)
    else:
        print 'Well, nothing was actually processed but you get a nice list!'
    return instr_files


def main(args):
    df = pd.DataFrame(columns=['file', 'class'])
    if not os.path.exists(args.outpath):
        os.mkdir(args.outpath)
    for it in args.instrtype:
        instr_files = select_instrument(args, it)
        temp_df = df.DataFrame([instr_files, [it]*len(instr_files)], columns=['file', 'class'])
        df.append(temp_df, ignore_index=True)
    df.to_csv('{}data_info'.format(args.outpath), sep='\t', encoding='utf-8')
    return 0  # done, yay!


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--instrtype', type=list, default=[''])
    parser.add_argument('--outpath', type=str, default='results')
    parser.add_argument('--threshold', type=int, default=-32)
    parser.add_argument('parallel', type=str, choices=['p', 's'], default='p')
    args = parser.parse_args()
    main(args)

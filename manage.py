"""A manage.py a la django, which is the master controller for all the parts.

Contains the following modes (See the function's descriptions
for more details):

 - prepare_audio
 - extract_features
 - train_model <param_file> <model_id>
 - eval_model <model_id>
 - analyze
 - clean
"""

import argparse
import logging
import sys

logger = logging.getLogger(__name__)


def prepare_audio(**kwargs):
    """Download, unzip, preprocess, and collect a pandas dataframe which
    references to all of your audio.

    Parameters
    ----------

    Returns
    -------
    status_code : int
    """
    return -1


def extract_features(*kwargs):
    """Extract features for every audio file from the cashed dataframe above.

    Parameters
    ----------

    Returns
    -------
    status_code : int
    """
    return -1


def train_model(param_file, model_id, **kwargs):
    """Trains a model using the hyperparameters given in the param_file.

    Parameters
    ----------
    param_file : str
        Full path to a file containing the hyperparameters for this run.

    model_id : str
        A name for this run which will define the output path for all
        intermediate files for this run.

    Returns
    -------
    status_code : int
    """
    return -1


def eval_model(model_id, **kwargs):
    """
    Evalute a model against a test set using the model_id.

    Parameters
    ----------
    model_id : str
        Name for this run. Loads the training parameters for evaluation
        using this. If no training parameters are set, fails.

    Returns
    -------
    status_code : int
    """
    return -1


def analyze(**kwargs):
    """This could launch an jupyter notebook session??
    I'm not sure yet how best to do this.
    """
    return -1


def clean(**kwargs):
    """Clean stuff so we can rerun it with a clean state."""
    return -1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="Increase the verbosity of program output. "
                             "-v=INFO, -vv=DEBUG")
    parser.add_argument("--pdb", action="store_true",
                        help="Launch pdb on fail")
    subparsers = parser.add_subparsers()

    prepare_audio_parser = subparsers.add_parser("prepare_audio")
    prepare_audio_parser.set_defaults(func=prepare_audio)
    extract_features_parser = subparsers.add_parser("extract_features")
    extract_features_parser.set_defaults(func=extract_features)
    train_model_parser = subparsers.add_parser("train_model")
    train_model_parser.set_defaults(func=train_model)
    eval_model_parser = subparsers.add_parser("eval_model")
    eval_model_parser.set_defaults(func=eval_model)
    analyze_parser = subparsers.add_parser("analyze")
    analyze_parser.set_defaults(func=analyze)
    clean_parser = subparsers.add_parser("clean")
    clean_parser.set_defaults(func=clean)

    args = vars(parser.parse_args())

    verbosity = args.pop('verbose', 0)
    logLevel = logging.WARNING
    if verbosity == 1:
        logLevel = logging.INFO
    elif verbosity >= 1:
        logLevel = logging.DEBUG
    # Set the logging verbosity.
    logging.basicConfig(level=logLevel)

    try:
        fx = args.pop('func')
    except KeyError:
        parser.print_help()
        sys.exit(-1)

    # Actually run your function now.
    try:
        sys.exit(fx(**args))
    except KeyboardInterrupt:
        logger.warning("User Cancelled... Done")
    except Exception as e:
        if 'pdb' in args and args['pdb'] is True:
            import pdb
            pdb.pm()
        else:
            raise e

Requirements Setup:

1. Install a miniconda
 See: http://conda.pydata.org/miniconda.html

2. Set up your ismir2016 conda env
```bash
 $ conda create -n ismir2016
 # Update Conda
 $ conda update conda
```

3. Activate your environment
`source activate ismir2016`

3. Install dependencies
pip install -r requirements.txt

4. Develop your code here:
`./deepclustering/*

5. Test your code like this:
`py.test` <-- run all the tests
`py.test --pdb` <-- Run it but fail out to the debugger.
`py.test deepclustering/tests/test_foo.py` <-- run a specific test file.

6. Use manage.py to run your code.
```bash
 $ python manage.py prepare_audio
 $ python manage.py extract_features
 $ python manage.py train_model <param_file> <model_id>
 $ python manage.py eval_model <model_id>
 $ python manage.py analyze
 $ python manage.py clean
```

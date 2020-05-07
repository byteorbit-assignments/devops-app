Dependencies
============
- Python 3.7+
- PostgreSQL 10+
- Redis

Installing Dependencies
=======================
- PostgreSQL server
    - MacOS: https://postgresapp.com/
    - Ubuntu: ``apt-get install postgresql``
- Redis
    - MacOS: https://bit.ly/2FeqVWf
    - Ubuntu: ``apt-get install redis-server``
- Python3
    - PyEnv (Linux or MacOS): https://github.com/pyenv/pyenv#installation
    - Homebrew (MacOS): ``brew install python3``            


Tests
=====
We use tox (see: `tox.ini`) to run the test suite. To run with your default py3:

    tox -r -e py3


Code Style
==========
Make sure code and test files are free of style errors by running flake8.
 
This runs on Jenkins too and style errors will fail the build.

Error code reference: https://pycodestyle.readthedocs.io/en/latest/intro.html#error-codes

    flake8 tests/ src/

You can also run this with tox:

    tox -r -e py3-flake8
    
Docker
======================
The docker-compose config will run by default with...
  - production mode server with compiled static assets
  - no code reload (restart on code changes)
  
Ensure you have the latest base image:
    
    docker-compose build --pull web

Run server:
 
    docker-compose up


#### Cleanup
Delete stale containers, images, volumes with:

    docker-compose down --volumes --remove-orphans --rmi local

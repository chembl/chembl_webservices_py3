FROM debian:jessie-slim

# revents Python from writing pyc files to disc and from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install required ubuntu packages
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends gcc libc-dev ca-certificates libxrender1 libxext6 wget bzip2 libgraphicsmagick++3 libopenbabel4 libpotrace0 && \
    apt-get -qq -y autoremove && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/* /var/log/dpkg.log

# install miniconda
RUN wget --quiet https://repo.continuum.io/miniconda/Miniconda3-4.7.12.1-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm -rf $HOME/conda/pkgs/* && \
    rm ~/miniconda.sh

# add conda bin to path
ENV PATH /opt/conda/bin:$PATH

# use the environment.yml to create the conda env
COPY environment.yml /tmp/environment.yml

# create the conda env using saved environment file
RUN conda env create -n chembl-webservices-py3 -f /tmp/environment.yml

# activate env (add conda env bin to path)
ENV PATH /opt/conda/envs/chembl-webservices-py3/bin:$PATH

# setup gunicorn log and pid folder
RUN mkdir gunicorn

# copy webservices code and config files
COPY gunicorn.conf.py gunicorn.conf.py
COPY src src
COPY manage.py manage.py

ENTRYPOINT [ "gunicorn", "-c", "gunicorn.conf.py", "chembl_ws_app.wsgi:application" ]
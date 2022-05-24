FROM python:3.10

WORKDIR /downleth

COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock
RUN pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

COPY ./downleth ./downleth
COPY ./setup.py ./README.md ./

RUN python setup.py install

ENTRYPOINT ["/bin/bash"]

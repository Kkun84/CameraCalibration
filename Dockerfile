FROM python

# for Timezone setting
RUN apt-get update && apt-get install -y tzdata

# apt-get install
RUN apt-get update && apt-get install -y fish nano git

# Install Python library
COPY requirements.txt /
RUN pip install -r /requirements.txt

ENV PYTHONPATH "${PYTONPATH}:/workspace"

WORKDIR /workspace

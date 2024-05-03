FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive
ARG PYTHON_VERSION=3.11.7
ARG HASS_BRANCH=2024.2.3

ENV PYENV_ROOT=/opt/pyenv
ENV PATH=${PYENV_ROOT}/bin:${PYENV_ROOT}/shims:${PATH}

COPY config/configuration.yaml /hass/

RUN apt-get update && \
	apt-get upgrade -y && \
	apt-get install -y --no-install-recommends \
	autoconf \
    bluez \
    build-essential \
    ca-certificates \
    cmake \
    curl \
    ffmpeg \
	git \
    libavcodec-dev \
    libavdevice-dev \
	libavfilter-dev \
    libavformat-dev \
    libavutil-dev \
    libbz2-dev \
	libffi-dev \
	libjpeg-dev \
	liblzma-dev \
    libncursesw5-dev \
    libpcap-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
	libswresample-dev \
	libswscale-dev \
	libudev-dev \
	libxml2-dev \
	libxmlsec1-dev \
	libxslt1-dev \
	libyaml-dev \
	pkg-config \
    tk-dev \
    xz-utils \
	zlib1g-dev

WORKDIR /opt

RUN git clone https://github.com/pyenv/pyenv.git && \
    echo 'eval "$(pyenv init -)"' >> /etc/profile && \
    pyenv install ${PYTHON_VERSION} && \
    pyenv global ${PYTHON_VERSION}

WORKDIR /opt/hass

RUN git clone --depth=1 https://github.com/home-assistant/core.git --branch ${HASS_BRANCH}

WORKDIR /opt/hass/core

RUN ./script/setup

WORKDIR /hass

EXPOSE 8123

FROM debian:bookworm-slim

# python user id is set at build time
ARG PYTHON_UID=1000

RUN  apt-get update \
  && apt-get install -y \
      jq \
      chromium \
      python3-pip \
      python3-venv \
      vim \
      fonts-noto-color-emoji \
      libenchant-2-2 \
      libevent-2.1-7 \
      libflite1 \
      libgraphene-1.0-0 \
      libgstreamer-gl1.0-0 \
      libgstreamer-plugins-bad1.0-0 \
      libgstreamer-plugins-base1.0-0 \
      libgstreamer1.0-0 \
      libgtk-4-1 \
      libharfbuzz-icu0 \
      libhyphen0 \
      libmanette-0.2-0 \
      libnghttp2-14 \
      libpsl5 \
      libvpx7 \
      libwebpdemux2 \
      libwebpmux3 \
      libwoff1 \
      libx264-164 \
  && rm -rf /var/lib/apt/lists/*

ADD https://raw.githubusercontent.com/thomas-is/rc/main/.vimrc /etc/vim/vimrc
RUN chmod 644 /etc/vim/vimrc

COPY ./docker-entrypoint.sh /usr/local/bin/
RUN chmod 755 /usr/local/bin/docker-entrypoint.sh

RUN  adduser --uid $PYTHON_UID --home /home/python --disabled-password python \
  && mkdir /home/python/videos \
  && chown python:python /home/python/videos \
  && mkdir /venv \
  && chown python:python /venv

COPY ./etc/bash.bashrc       /home/python/.bashrc
COPY ./etc/bash.bash_aliases /home/python/.bash_aliases
RUN  chown python:python /home/python/.bashrc \
  && chmod 644 /home/python/.bashrc \
  && chown python:python /home/python/.bash_aliases \
  && chmod 644 /home/python/.bash_aliases

COPY ./src /src
RUN  chown -R python:python /src

USER python
WORKDIR /src

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install -U \
      pip \
      setuptools \
      wheel
RUN  pip install -r requirements.txt  \
  && playwright install


ENTRYPOINT [ "/usr/local/bin/docker-entrypoint.sh" ]
CMD [ "/bin/bash", "-l" ]
VOLUME [ "/home/python/videos" ]

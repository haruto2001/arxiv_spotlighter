ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-slim-bookworm

ARG USERNAME=user

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV RYE_HOME /home/${USERNAME}/.rye
ENV PATH ${RYE_HOME}/shims:${PATH}

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        gosu && \
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/*

# ARG USERNAME=user
RUN adduser --disabled-password --gecos "" ${USERNAME}

SHELL [ "/bin/bash", "-o", "pipefail", "-c" ]
RUN curl -sSf https://rye.astral.sh/get | RYE_NO_AUTO_INSTALL=1 RYE_INSTALL_OPTION="--yes" bash && \
    rye config --set-bool behavior.global-python=true && \
    rye config --set-bool behavior.use-uv=true && \
    rye pin ${PYTHON_VERSION}

RUN mkdir /workspace
WORKDIR /workspace

# COPY pyproject.toml requirements.lock requirements-dev.lock .python-version README.md ./

RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=requirements.lock,target=requirements.lock \
    --mount=type=bind,source=requirements-dev.lock,target=requirements-dev.lock \
    --mount=type=bind,source=.python-version,target=.python-version \
    --mount=type=bind,source=README.md,target=README.md \
    rye sync --no-dev --no-lock

COPY . .

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

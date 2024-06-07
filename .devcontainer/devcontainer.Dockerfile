FROM python:3.12-slim

RUN mkdir -p /workspace

ARG UID=1000

ARG GID=1000

RUN groupadd -f -o -r -g $GID vscode && useradd -ms /bin/bash -o -u $UID -g $GID vscode

RUN chown -R vscode:vscode /workspace

RUN apt-get update \
    && apt-get -y install fontconfig fonts-powerline curl git jq \
    && rm -rf /var/lib/apt/lists/*

RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && mkdir /commandhistory \
    && touch /commandhistory/.bash_history \
    && chown -R vscode:vscode /commandhistory \
    && echo "$SNIPPET" >> "/home/vscode/.bashrc"

USER vscode

RUN curl -sSL https://pdm-project.org/install-pdm.py | python -

RUN curl -fsSL https://raw.githubusercontent.com/pressly/goose/master/install.sh | GOOSE_INSTALL=/home/vscode/.local sh

RUN <<PDMSHELL cat >> /home/vscode/.bashrc
pdm() {
  local command=\$1
  if [[ "\$command" == "shell" ]]; then
    eval \$(pdm venv activate)
  else
    command pdm \$@
  fi
}
PDMSHELL

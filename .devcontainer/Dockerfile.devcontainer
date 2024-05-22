FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

ARG USERNAME=vscode

RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && mkdir /commandhistory \
    && touch /commandhistory/.bash_history \
    && chown -R $USERNAME /commandhistory \
    && echo "$SNIPPET" >> "/home/$USERNAME/.bashrc" \
    && pipx install "pdm~=2.15"

COPY install-goose.sh /tmp/install-goose.sh

RUN chmod +x /tmp/install-goose.sh && /tmp/install-goose.sh && rm -f /tmp/install-goose.sh

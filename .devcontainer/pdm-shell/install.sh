#!/bin/sh
set -e

echo "Activating feature 'pdm-shell'"
echo "User: ${_REMOTE_USER}     User home: ${_REMOTE_USER_HOME}"

if [  -z "$_REMOTE_USER" ] || [ -z "$_REMOTE_USER_HOME" ]; then
  echo "***********************************************************************************"
  echo "*** Require _REMOTE_USER and _REMOTE_USER_HOME to be set (by dev container CLI) ***"
  echo "***********************************************************************************"
  exit 1
fi

# Set pdm func for zsh
cat << EOF >> "$_REMOTE_USER_HOME/.zshrc"
pdm() {
  local command=\$1

  if [[ "\$command" == "shell" ]]; then
      eval \$(pdm venv activate)
  else
      command pdm \$@
  fi
}
EOF
chown -R $_REMOTE_USER $_REMOTE_USER_HOME/.zshrc

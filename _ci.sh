#!/usr/bin/env bash
echo "=============================================================="
echo "BASH_VERSION" $BASH_VERSION
echo $(git --version)
com="$(git rev-parse HEAD)"
msg=$(git log -1 --pretty=%B)
echo "=============================================================="
echo "Establish git variables:"
echo "=============================================================="
echo "Current commit hash : $com"
echo "Commit msg          : $msg"
echo "=============================================================="
echo "Environment variables:"
echo "=============================================================="
echo "CI                   = $CI"
echo "APPVEYOR             = $APPVEYOR"
echo "CIRCLECI             = $CIRCLECI"
echo "TRAVIS               = $TRAVIS"
echo "CODESHIP             = $CI_NAME"
echo "=============================================================="
if [[ $CI = true ]]||[[ $CI = True ]]
then
    sudo wget --quiet https://github.com/jgm/pandoc/releases/download/1.19.2.1/pandoc-1.19.2.1-1-amd64.deb -O _pandoc.deb
    sudo dpkg -i _pandoc.deb
    sudo apt-get update -y
    sudo apt-get install texlive-xetex texlive-latex-recommended texlive-fonts-recommended texlive-latex-extra python-software-properties
    pip install -I dropbox
    pip install jupyter
    sudo add-apt-repository -y ppa:libreoffice/ppa
    sudo apt-get update -y
    sudo apt-get install -y libreoffice-writer libreoffice-impress libreoffice-calc  
else
    echo "Not running on CI server, probably running on local computer"
    python .continuous_integration/convert_and_send_to_dropbox.py
fi

#!/bin/bash
function install()
{
    echo "Archiving and extracting setup project from git."
    echo "-----------------------------------------------"
    git archive --format=zip --remote=git@gitlab.com:vamsy-krishna/DjangoPythonProjectSkeleton.git develop > setup.zip
    unzip setup.zip -d setup
    echo ""
    echo "Provisioning."
    echo "------------"
    cd setup/ && vagrant up
}

# Handle command argument
case "$1" in
    install) install;;
    *) wrong_command $1;;
esac

#!/bin/bash

# highly modified version of:
# https://www.pythonguis.com/tutorials/packaging-pyside6-applications-pyinstaller-macos-dmg/
# amoung others... including
# https://pyinstaller.org/en/stable/

pushd ..

#if doesn't the packenv directory doesn't exist...
directory="./packenv"
actfile="./packenv/bin/activate"
if [ ! -d "$directory" ]  || [ ! -f "$actfile" ] ; then
   python3 -m venv packenv
   source packenv/bin/activate

   pip install --upgrade pip
   pip install PyInstaller
else
   source packenv/bin/activate
fi

cp BuildScripts/build.ubuntu2404.spec jenkinsTools

pushd vmm

pyinstaller --clean -y build.ubuntu2404.spec
pyinstaller -y build.ubuntu2404.spec


rm build.ubuntu2404.spec

popd
popd



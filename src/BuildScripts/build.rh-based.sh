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
   pip install python-jenkins
   pip install PyInstaller
else
   source packenv/bin/activate
fi

cp BuildScripts/build.rh-based.spec jenkinsTools

pushd vmm

pyinstaller --clean -y build.rh-based.spec

pyinstaller -y build.rh-based.spec

rm build.rh-based.spec

popd
popd



#!/bin/bash

sudo yum -y update 
sudo yum -y install wget gcc gcc-c++ python-devel findutils zlib-devel zip openssl-devel bzip2-devel libffi-devel 
mkdir Python373 
pushd Python373 
wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz 
tar zxf Python-3.7.3.tgz 
pushd Python-3.7.3 
sudo ./configure --enable-optimizations 
sudo make altinstall 
popd
popd
sudo /usr/local/bin/pip3.7 install virtualenv 
virtualenv -p /usr/local/bin/python3.7 env 
source env/bin/activate 
pip3.7 install cython 
wget https://github.com/AvivAvital2/Saucer/archive/master.zip -P Saucer 
pushd Saucer 
unzip master.zip 
pushd Saucer-master 
pip3.7 install -r requirements.txt 
python setup.py bdist_wheel 
pip3.7 install dist/spacy*.whl 
popd
mkdir python 
pushd python 
cp -R $VIRTUAL_ENV/lib/python3.7/site-packages/* . >& /dev/null 
for i in `find . -name "*.so"`; do echo $i; strip $i; done 
for i in `find . -name "*.so.*"`; do echo $i; strip $i; done 
rm -fdr wheel* pip* easy_install.py* 
find . | grep pyc$ | xargs rm -fdr 
zip -FS -r9 ../Saucer3.zip * 
popd
zip -r9 Saucer3_layer.zip python/ 
mv Saucer3_layer.zip ../
popd
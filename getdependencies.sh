# Download azcopy
wget -q -O azcopy_linux.tar.gz https://aka.ms/downloadazcopy-v10-linux
tar -xvzf azcopy_linux.tar.gz --wildcards */azcopy --strip 1
rm azcopy_linux.tar.gz
chmod u+x azcopy
pip install pandas Pillow torch torchvision tqdm 

# for notebooks: %%bash
#Dependencies
# Download azcopy
wget -q -O azcopy_linux.tar.gz https://aka.ms/downloadazcopy-v10-linux
tar -xvzf azcopy_linux.tar.gz --wildcards */azcopy --strip 1
rm azcopy_linux.tar.gz
chmod u+x azcopy
# Get Images
PATH_URL="https://lilablobssc.blob.core.windows.net/snapshot-safari/KGA/"
DATASET_DIR="KGA_S1.lila.zip"
DATASET="/content/snapshot-kgalagadi-images"
./azcopy cp "${PATH_URL}${DATASET_DIR}" "${DATASET}.zip" --recursive
# Get Annotations
ANNOTATIONS_DIR="SnapshotKgalagadi_S1_v1.0.json.zip"
ANNOTATIONS="/content/snapshot-kgalagadi-annotations"
./azcopy cp "${PATH_URL}${ANNOTATIONS_DIR}" "${ANNOTATIONS}.zip" --recursive
#make dir and unzip
mkdir "/content/${ANNOTATIONS}"
mkdir "/content/${DATASET}"
unzip "${ANNOTATIONS}.zip" -d "${ANNOTATIONS}"
unzip "${DATASET}.zip" -d "${DATASET}"
# Dependencies
pip install pandas Pillow torch torchvision tqdm 

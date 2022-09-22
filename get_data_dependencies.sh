# Takes URL DATASETPATH ANNOTATIONSPATH DATASETLOCAL ANNOTATIONSLOCAL  
#Dependencies
# Download azcopy
wget -q -O azcopy_linux.tar.gz https://aka.ms/downloadazcopy-v10-linux
tar -xvzf azcopy_linux.tar.gz --wildcards */azcopy --strip 1
rm azcopy_linux.tar.gz
chmod u+x azcopy
# Get Images
PATH_URL=$1
DATASET_DIR=$2
DATASET=$4
ANNOTATIONS_DIR=$3
ANNOTATIONS=$5
./azcopy cp "${PATH_URL}${DATASET_DIR}" "${DATASET}.zip" --recursive
./azcopy cp "${PATH_URL}${ANNOTATIONS_DIR}" "${ANNOTATIONS}.zip" --recursive
#make dir and unzip
mkdir "${ANNOTATIONS}"
mkdir "${DATASET}"
unzip "${ANNOTATIONS}.zip" -d "${ANNOTATIONS}"
unzip "${DATASET}.zip" -d "${DATASET}"
rm "${ANNOTATIONS}.zip"
rm "${DATASET}.zip"
# Dependencies
pip install pandas Pillow torch torchvision tqdm 
REPO="https://raw.githubusercontent.com/1795757/csl/main/"
declare -a TODOWNLOAD=("unpack_format.py")
for file in "${TODOWNLOAD[@]}"
do
  wget -q -O i "${REPO}${file}"
done

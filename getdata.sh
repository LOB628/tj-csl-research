# Takes URL DATASETPATH ANNOTATIONSPATH DATASETLOCAL ANNOTATIONSLOCAL  
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

#!/bin/bash
# update_repo_list.sh - Update a list of repo contents on s3 on the AARNet UAT stratum 1 CVMFS server
# N.B: THIS SCRIPT WILL NOT WORK ON A CLIENT SYSTEM - it is included for completeness only

# Read CVMFS S3 config
. /etc/cvmfs/s3.conf

export AWS_ACCESS_KEY_ID="${CVMFS_S3_ACCESS_KEY}"
export AWS_SECRET_ACCESS_KEY="${CVMFS_S3_SECRET_KEY}"
export AWS_DEFAULT_REGION="${CVMFS_S3_REGION}"

AWS_CLI_PATH="/usr/local/bin/aws"
REPO="singularity.galaxyproject.org"
SUBDIRECTORY="all"
LISTFILE="/tmp/${REPO}_list.txt"
KEY="${REPO}/${REPO}_list.txt"
OBJECT="s3://${CVMFS_S3_BUCKET}/${KEY}"

if [ ! -d "/cvmfs/${REPO}/${SUBDIRECTORY}" ]
then
  echo "CVMFS Directory /cvmfs/${REPO}/${SUBDIRECTORY} does not exist."
  exit 1
fi

echo "Updating list at https://${CVMFS_S3_BUCKET}.s3.${CVMFS_S3_REGION}.amazonaws.com/${KEY}"

ls --full-time -s /cvmfs/${REPO}/${SUBDIRECTORY} | awk '{print $10 " " $6 " " $7 " " $8}' > ${LISTFILE}
echo "Created file ${LISTFILE}"

${AWS_CLI_PATH} s3 cp --quiet ${LISTFILE} ${OBJECT}
echo "Copied file ${LISTFILE} to object ${OBJECT}"

${AWS_CLI_PATH} s3api put-object-acl --bucket ${CVMFS_S3_BUCKET} --key ${KEY} --acl public-read
echo "Object ${OBJECT} made publicly readable"

echo "Updated list can be accessed at https://${CVMFS_S3_BUCKET}.s3.${CVMFS_S3_REGION}.amazonaws.com/${KEY}"

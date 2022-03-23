#!/bin/bash

if [[ "$1" == "down" ]]; then
    echo "Destroying..."
    terraform -chdir=deployment destroy --auto-approve
    exit 0
fi


BUILD_DIR=./.build
CURRENT_DIR=$(pwd)
PYTHON_RUNTIME=python3.8
VENV=$BUILD_DIR/venv
# Create a temp virtual env for the deployment
python3 -m venv $VENV


mkdir $BUILD_DIR
mkdir $BUILD_DIR/app_pkg

# Install dependencies
$VENV/bin/pip install --upgrade pip \
    && $VENV/bin/pip install -r requirements.txt \
    && cp -r $VENV/lib/$PYTHON_RUNTIME/site-packages/ $BUILD_DIR/app_pkg \
    && cp -r ./src/ $BUILD_DIR/app_pkg/ \
    && rm -fr $BUILD_DIR/venv \
    && terraform -chdir=deployment init \
    && terraform -chdir=deployment apply --auto-approve \
    && rm -fr $BUILD_DIR \
    && echo "Deployment completed!!!"


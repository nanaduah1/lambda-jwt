#!/bin/bash


BUILD_DIR=./.build
LAMBDAFY="$BUILD_DIR/lambdafy"
CURRENT_DIR=$(pwd)
PYTHON_RUNTIME=python3.8
VENV=$BUILD_DIR/venv
# Create a temp virtual env for the deployment
python3 -m venv $VENV


if [[ "$1" == "down" ]]; then
    echo "Destroying..."
    terraform -chdir=$LAMBDAFY destroy --auto-approve
    exit 0
fi

if [ ! -d "$LAMBDAFY" ]; then
   git clone https://github.com/nanaduah1/infra4  $BUILD_DIR/infra4 \
        && mkdir $BUILD_DIR/app_pkg \
        && cp -r  $BUILD_DIR/infra4/lambdafy $BUILD_DIR \
        && rm -fr $BUILD_DIR/infra4
fi

# Install dependencies
$VENV/bin/pip install --upgrade pip \
    && $VENV/bin/pip install -r requirements.txt \
    && cp -r $VENV/lib/$PYTHON_RUNTIME/site-packages/ $BUILD_DIR/app_pkg \
    && cp -r ./src/ $BUILD_DIR/app_pkg/ \
    && rm -fr $BUILD_DIR/venv \
    && export TF_VAR_build_dir=$(realpath $BUILD_DIR) \
    && terraform -chdir=$LAMBDAFY init \
    && terraform -chdir=$LAMBDAFY apply --auto-approve \
    && rm -fr $BUILD_DIR/app_pkg/* \
    && rm $BUILD_DIR/app_pkg.zip \
    && echo "Deployment completed!!!"


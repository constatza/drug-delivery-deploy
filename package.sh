#!/usr/bin/env bash

# This script is used to package the application for distribution.
rsync -av ../DrugDeliveryModel/bin/Release/net8.0/linux-x64/publish/ ./app
rsync -av ../DrugDeliveryModel/Input/ ./Input

rsync -avzP --delete \
  --exclude '.idea/' \
  --exclude 'scripts/myenv/'\
  . meluxina:~/apps/drug-delivery-model

#!/usr/bin/env bash

# This script is used to package the application for distribution.
rsync -av ../DrugDeliveryModel/bin/Release/net8.0/linux-x64/publish/ ./app
rsync -av ../DrugDeliveryModel/Input/ ./Input

rsync -avzP --delete \
  --exclude '.idea/' \
  --exclude 'scripts/myenv/'\
  --exclude 'scripts/slurm/'\
  --exclude 'Output/'\
  --exclude 'config-auto-generated/'\
  . meluxina:~/apps/drug-delivery-model

rsync -avzP meluxina:~/apps/drug-delivery-model/Output/metadata/ Output/metadata

rsync -avzP --exclude '*/' meluxina:~/apps/drug-delivery-model/Output/12EquationsSmall/ Output/12EquationsSmall
rsync -avzP --exclude '*/' meluxina:~/apps/drug-delivery-model/Output/12EquationsLarge/ Output/12EquationsLarge
rsync -avzP --exclude '*/' meluxina:~/apps/drug-delivery-model/Output/12EquationsMedium/ Output/12EquationsMedium
rsync -avzP --exclude '*/' meluxina:~/apps/drug-delivery-model/Output/5EquationsSmall/ Output/5EquationsSmall
rsync -avzP --exclude '*/' meluxina:~/apps/drug-delivery-model/Output/5EquationsMedium/ Output/5EquationsMedium
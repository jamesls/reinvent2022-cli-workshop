#!/bin/bash
copilot app init cli-workshop-app
# As far as I can tell `--default-config` is a lie, it won't
# touch the environment manifest file if it already exists,
# we just need to specify it so it doesn't prompt us.
copilot env init --name dev --profile burner --default-config
copilot env init --name prod --profile burner --default-config
copilot env deploy --name dev
copilot env deploy --name prod
copilot svc init --name cli-workshop-svc
copilot svc deploy --name cli-workshop-svc --env dev

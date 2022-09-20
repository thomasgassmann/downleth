#!/bin/bash

npx ts-json-schema-generator -p config.schema.ts --no-top-ref -t Config > config.schema.json

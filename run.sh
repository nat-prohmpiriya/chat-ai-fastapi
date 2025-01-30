#!/bin/bash

pipenv run uvicorn src.main:app --reload --port 5001

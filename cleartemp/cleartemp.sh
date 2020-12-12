#!/usr/bin/env bash
find /home/site/wwwroot/downloads/tmp* -maxdepth 0 -mmin +5 -exec rm -fr {} +;

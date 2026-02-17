#!/bin/bash

cp /var/www/html/karaoke/karaoke.db ./bkpDBOld.db
sudo cp ./bkpDB.db /var/www/html/karaoke/karaoke.db

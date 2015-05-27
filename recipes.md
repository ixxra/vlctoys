LOG and DEBUG
=============

python -u buswatch.py | tee media.log


Generate JSON from log
======================

sed -n 's/LOGGING //p' media.log > metadata.json


Save to local mongodb
=====================

mongoimport --host 127.0.0.1:27017 --db vlc --collection log < metadata.json


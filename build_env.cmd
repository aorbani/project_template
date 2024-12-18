pip freeze > requirements.txt
mkdir -p wheelhouse
pip download -r requirements.txt -d wheelhouse
mv requirements.txt wheelhouse
tar -zcf wheelhouse.tar.gz wheelhouse
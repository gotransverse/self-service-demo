

BASEDIR=`/Users/mswanholm $0`/..
DEMODIR=`/Users/mswanholm/self-service $0`/..

if [ ! -d "$BASEDIR/demoEnv" ]; then
    virtualenv -q -p python3 $BASEDIR/demoEnv --no-site-packages
    echo "Virtualenv created."
fi

if [ ! -f "$BASEDIR/demoEnv/updated" -o $BASEDIR/requirements.txt -nt $BASEDIR/demoEnv/updated ]; then
    pip install -r $BASEDIR/requirements.txt -E $BASEDIR/demoEnv
    touch $BASEDIR/demoEnv/updated
    echo "Requirements installed."
fi

$BASEDIR/bin/setup

source $BASEDIR/demoEnv/bin/activate
cd $BASEDIR
export PYTHONPATH=.

#exec python3 $DEMODIR/run_demo.py

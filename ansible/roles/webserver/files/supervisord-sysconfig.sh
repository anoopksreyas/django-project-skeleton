# this is sourced by the supervisord init script

set -a

# should probably put both of these options as runtime arguments
OPTIONS="-c /etc/supervisord/supervisord.conf"
PIDFILE=/var/run/supervisord.pid

# unset this variable if you don't care to wait for child processes to shutdown
# before removing the /var/lock/subsys/supervisord lock
WAIT_FOR_SUBPROCESSES=yes

# remove this if you manage number of open files in some other fashion
# ulimit -n 96000

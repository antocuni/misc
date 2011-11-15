#!/bin/sh

# create the checkwl.sh script
cat > /var/checkwl.sh <<EOF
#!/bin/sh
# script to be run on the router: it periodically does "ifconfig wl0 down &&
# up", unless there are wifi clients associated.  This is a workaround to
# revive the wifi lan if it crashes (which happens a lot, it seems)

while true
do
    N=\`wlctl assoclist | wc -l\`
    date > /var/checkwl.log
    if [ \$N -eq 0 ]
    then
        echo "no clients, restarting wifi" >> /var/checkwl.log
        ifconfig wl0 down && ifconfig wl0 up
    else
        echo "wifi clients found, good :-)" >> /var/checkwl.log
    fi
    sleep 30
done
EOF

# execute it
sh /var/checkwl.sh &

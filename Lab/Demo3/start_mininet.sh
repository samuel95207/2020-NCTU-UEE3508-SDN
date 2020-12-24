sudo mn --topo mytopo \
        --custom topo-4sw-6host.py \
        --controller remote \
        --switch default,protocols=OpenFlow13 \
        --link=tc
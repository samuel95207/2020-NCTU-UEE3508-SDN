# Copyright (C) 2016 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from operator import attrgetter

from ryu.app import simple_switch_13
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub


class SimpleMonitor13(simple_switch_13.SimpleSwitch13):

    def __init__(self, *args, **kwargs):
        super(SimpleMonitor13, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)

    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(5)

    def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # req = parser.OFPFlowStatsRequest(datapath)
        # datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)



    # @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    # def _flow_stats_reply_handler(self, ev):
    #     body = ev.msg.body

    #     self._flow_sw = ev.msg.datapath.id
    
    #     for stat in sorted([flow for flow in body if flow.priority == 1],
    #                        key=lambda flow: (flow.match['in_port'],
    #                                          flow.match['eth_dst'])):
    #         self._flow_dict[stat.match['eth_dst']] = stat.instructions[0].actions[0].port
        



    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        body = ev.msg.body

        sw_id = ev.msg.datapath.id
        port_dict = {}

        for stat in sorted(body, key=attrgetter('port_no')):
            if(stat.port_no == 4294967294):
                continue
            port_dict[stat.port_no] = {'tx_packets':stat.tx_packets,
                                       'rx_packets':stat.rx_packets}

        self.logger.info('--------------------------------')
        self.logger.info('SW id: %d\n',sw_id)
        for item in port_dict.items():
            self.logger.info('port: %d',item[0])
            self.logger.info('tx_packets: %d',item[1]['tx_packets'])
            self.logger.info('rx_packets: %d',item[1]['rx_packets'])
            self.logger.info(' ')

        self.logger.info('Address\t\t\tPort')
        if(format(sw_id, "d").zfill(16) in self.mac_to_port):
            for item in self.mac_to_port[format(sw_id, "d").zfill(16)].items():
                self.logger.info('%17s\t%d',item[0],item[1])
            self.logger.info('--------------------------------\n')




        

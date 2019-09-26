#!/usr/bin/env python
#
# little flow exporter
# read from amqp, exposes metrics in prometheus format
#

import sys
import pika
import json
from prometheus_client import start_http_server, Gauge

# read the configuration file
execfile('/etc/sfacctd/scripts/flows.conf')

# metrics
as_bps = Gauge('as_bps', 'as trafic trafic bits per seconds', ['direction', 'asn'])
as_pps = Gauge('as_pps', 'as trafic trafic packets per seconds', ['direction', 'asn'])
host_bps = Gauge('host_bps', 'host trafic bits per seconds', ['direction', 'host'])
host_pps = Gauge('host_pps', 'host trafic packets per seconds', ['direction', 'host'])
if_bps = Gauge('if_bps', 'interface trafic bits per seconds', ['direction', 'interface', 'router'])
if_pps = Gauge('if_pps', 'interface trafic packets per seconds', ['direction', 'interface', 'router'])
if_as_bps = Gauge('if_as_bps', 'as trafic bits per seconds by interface', ['direction', 'asn', 'interface'])
if_as_pps = Gauge('if_as_pps', 'as trafic paclets per seconds by interface', ['direction', 'asn', 'interface'])


class flow_consumer(object):

  def consume_data(self, channel, method, properties, body):

    data = json.loads(body)

    for line in data:

      # common fields
      bps = float(line['bytes']*8*sampling/interval)
      pps = float(line['packets']*sampling/interval)

      # routing key is normalized
      try:
        a, stype, direction = method.routing_key.split('_')
      except ValueError, e:
        print("Bad routing key %s" % str(e))
        continue

      if stype == 'as':
        asn = line['as_src'] if direction == 'in' else line['as_dst']
        as_bps.labels(direction, asn).set(bps)
        as_pps.labels(direction, asn).set(pps)
        continue

      if stype == 'host':
        host = line['ip_dst'] if direction == 'in' else line['ip_src']
        host_bps.labels(direction, host).set(bps)
        host_pps.labels(direction, host).set(pps)
        continue

      # map interface/hostname
      try:
        interface = interfaces_map[line['tag']]
        router = routers_map[line['tag']]
      except KeyError, e:
        print("Interface/Router not declared %s" % str(e))
        continue

      if stype == 'if':
        if_bps.labels(direction, interface, router).set(bps)
        if_pps.labels(direction, interface, router).set(pps)
        continue

      if stype == 'asif':
        asn = line['as_src'] if direction == 'in' else line['as_dst']
        if_as_bps.labels(direction, asn, interface).set(bps)
        if_as_bps.labels(direction, asn, interface).set(bps)
        continue


  def __init__(self):

    self.amqp_credential = pika.PlainCredentials(amqp['user'], amqp['pass'])
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=amqp['host'], credentials=self.amqp_credential))
    self.channel = self.connection.channel()
    self.channel.exchange_declare(exchange=amqp['exchange'], type='direct')

    for rk in rks:
      result = self.channel.queue_declare(exclusive=True)
      queue_name = result.method.queue
      self.channel.queue_bind(exchange=amqp['exchange'], routing_key=rk, queue=queue_name)
      self.channel.basic_consume(self.consume_data, queue=queue_name, no_ack=True)
    self.channel.start_consuming()

   
if __name__ == "__main__":
  start_http_server(8000)
  flow_consumer() 


#! /usr/bin/env python3

import sys
import time
import socket
import openpyxl


def parse_and_import_file(config):
  workbook = openpyxl.load_workbook(config['data_file'])
  worksheet = workbook.active
  for row in worksheet.values:
    parse_and_import_row(config, row)


def parse_and_import_row(config, row):
  try:
    data = parse_row(config, row)
  except Exception as e:
    print("Skipping unparseable row '{}': {}".format(row, e))
    return

  try:  
    import_data(config, data)
  except Exception as e:
    print("Problem importing row '{}': {}".format(row, e))


def parse_row(config, row):
  data = {}
  data['timestamp'] = int(time.mktime(time.strptime(row[0], '%Y-%m-%d %H:%M')))
  data['watts'] = row[1] * 1000
  return data


def import_data(config, data):
  msg = "{} {:0.0f} {:d}\n".format(config['metric_path'], data['watts'], data['timestamp'])
  print("importing to {}:{}  [{}]".format(config['graphite_host'], config['graphite_port'], msg.replace('\n', '')), flush = True)
  sock = socket.socket()
  sock.connect((config['graphite_host'], config['graphite_port']))
  sock.sendall(msg.encode())
  sock.close()


def main(argv):
  if len(argv) < 3:
    print("python ./import_el.py [excel_file] [graphite_host]")
    sys.exit(2)

  config = {}
  config['data_file'] = argv[1]
  config['graphite_host'] = argv[2]
  config['graphite_port'] = 2003
  config['metric_path'] = 'energy.household.total.watthours.count'

  parse_and_import_file(config)


main(sys.argv)

from xml.etree import ElementTree
import xml.etree.ElementTree as ET
import csv
import requests
import re
import sys
import requests.packages.urllib3
import time
from datetime import datetime


# Get XML Response from API
def reqpathmon(apikey, host):
    xml_blob = "<show><sdwan><path-monitor><stats/></path-monitor></sdwan></show>"
    #print xml_blob
    call = "https://%s/api/?type=op&cmd=%s&key=%s" % (host, xml_blob, apikey)
    #print(call)
    requests.packages.urllib3.disable_warnings()
    fw_results = requests.get(call, verify=False)
    #print(fw_results.content)
    #tree = ET.parse(fw_results.text)
    #print(tree)
    f = open('pathmon3.xml', 'w')
    f.write(fw_results.text)
    f.close()

    xml = ElementTree.parse("pathmon3.xml")
    root = xml.getroot()
    stats_list = root[0][0][1]  #move to subElement of root
    #print(stats_list.tag)
    current_date_time = datetime.now()
    
    # CREATE CSV FILE
    #csvfile = open("data.csv",'a',encoding='utf-8')
    #csvfile_writer = csv.writer(csvfile)
    
    # ADD THE HEADER TO CSV FILE
    # csvfile_writer.writerow(["vif_name","if_id","state_reason","state_change","latency","jitter","loss","if_name","profile"])
    
    # FOR EACH EMPLOYEE
    for entry in stats_list.findall("entry"):
        
        if(entry):
           
           # EXTRACT EMPLOYEE DETAILS  
          vif_name = entry.find("vif_name")
          if_id = entry.find("if_id")
          state_reason = entry.find("state_reason")
          state_change = entry.find("state_change")
          latency = entry.find("latency")
          jitter = entry.find("jitter")
          loss = entry.find("loss")
          if_name = entry.find("if_name")
          profile = entry.find("profile")
          
          file_name = if_id.text
          #print(file_name)
          csvfile = open("%s.csv" % file_name,'a',encoding='utf-8')
          csvfile_writer = csv.writer(csvfile)
    
          csv_line = [current_date_time, vif_name.text, if_id.text, state_reason.text, state_change.text, latency.text, jitter.text, loss.text, if_name.text, profile.text]
    
          # ADD A NEW ROW TO CSV FILE
          csvfile_writer.writerow(csv_line)



lhost = "sdwan.demo.net"
lapikey = "*********************************"

while(True):
   reqpathmon(lapikey, lhost)
   time.sleep(5)



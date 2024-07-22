import os
import sys
import xml.etree.ElementTree as ET

predefined_core_dict = {
                        'fs.defaultFS': 'hdfs://namenode:9000',
                         'hadoop.tmp.dir': '/hadoop/tmp',
                         'io.file.buffer.size': '131072',
                         }
predefined_hdfs_dict = {
                         'dfs.replication': '2',
                         'dfs.blocksize': '134217728',
                         'dfs.namenode.name.dir': '/hadoop/dfs/name',
                         }
predefined_mapred_dict = {'mapreduce.framework.name': 'yarn',
                           'mapreduce.jobhistory.address': 'namenode:10020',
                           'mapreduce.task.io.sort.mb': '256',
                           }

predefined_yarn_dict = { 
                        'yarn.resourcemanager.address': 'namenode:8032',
                         'yarn.nodemanager.resource.memory-mb': '8192',
                         'yarn.scheduler.minimum-allocation-mb': '1024',
                         }

def main():
    xml_path = sys.argv[1:][0]
    file_name = xml_path.split('/')[-1][:-4]
    
    if file_name == "core-site":
        info = predefined_core_dict
    elif file_name == "hdfs-site":
        info = predefined_hdfs_dict
    elif file_name == "mapred-site":
        info = predefined_mapred_dict
    elif file_name == "yarn-site":
        info = predefined_yarn_dict
    else:
        raise NotImplemented("Wrong config file path!")

    tree = ET.parse(xml_path)
    root = tree.getroot()

    for key, value in info.items():
        updated = 0
        for property in root.findall('property'):
            # using root.findall() to avoid removal during traversal
            name = property.find('name').text
            if name == key:
                property.find('value').text = value
                updated = 1
        if not updated:
            obj = ET.SubElement(root, 'property')
            ET.SubElement(obj, 'name').text = key
            ET.SubElement(obj, 'value').text = value
          
    tree.write(xml_path, encoding='UTF-8', xml_declaration=True)
    return 

if __name__=="__main__":
    main()
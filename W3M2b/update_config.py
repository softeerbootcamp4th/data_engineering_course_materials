import os
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import shutil
import subprocess

def delete_files(file_names, directory):
    for file_name in file_names:
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"파일이 삭제되었습니다: {file_name}")
        else:
            print(f"파일이 존재하지 않습니다: {file_name}")

def backup_files(file_names, directory):
    for file_name in file_names:
        original_file = os.path.join(directory, file_name)
        backup_file = f"{original_file}.bak"
        if os.path.isfile(original_file):
            shutil.copy2(original_file, backup_file)
            print(f"백업 성공: {backup_file}")
        else:
            print(f"파일이 존재하지 않습니다: {original_file}")

def save_new_config(config_updates, directory):
    def dict_to_xml(tag, d):
        elem = Element(tag)
        for key, val in d.items():
            child = SubElement(elem, 'property')
            name = SubElement(child, 'name')
            name.text = str(key)
            value = SubElement(child, 'value')
            value.text = str(val)
        return elem

    def save_config_xml(config, filename):
        xml_element = dict_to_xml('configuration', config)
        xml_str = tostring(xml_element, 'utf-8')
        pretty_xml_str = parseString(xml_str).toprettyxml(indent="    ")
        with open(os.path.join(directory, filename), 'w') as f:
            f.write(pretty_xml_str)

    for filename, config in config_updates.items():
        save_config_xml(config, filename)

if __name__ == "__main__":

    hadoop_config_directory = "/usr/local/hadoop/etc/hadoop"
    config_files = ["core-site.xml", "hdfs-site.xml", "mapred-site.xml", "yarn-site.xml"]
    
    ##### -site.xml 백업
    backup_files(config_files, hadoop_config_directory)

    ##### -site.xml 삭제
    delete_files(config_files, hadoop_config_directory)

    ##### 설정으로 xml 파일 생성
    config_updates = {
        "core-site.xml": {
            "fs.defaultFS": "hdfs://hadoop-master:9000",
            "hadoop.tmp.dir": "file:///usr/local/hadoop/tmp",
            "io.file.buffer.size": "131072"
        },
        "hdfs-site.xml": {
            "dfs.replication": "2",
            "dfs.blocksize": "134217728",
            "dfs.namenode.name.dir": "file:///usr/local/hadoop/dfs/name"
        },
        "mapred-site.xml": {
            "mapreduce.framework.name": "yarn",
            "mapreduce.jobhistory.address": "hadoop-master:10020",
            "mapreduce.task.io.sort.mb": "256"
        },
        "yarn-site.xml": {
            "yarn.resourcemanager.address": "hadoop-master:8032",
            "yarn.nodemanager.resource.memory-mb": "8192",
            "yarn.scheduler.minimum-allocation-mb": "1024"
        }
    }

    save_new_config(config_updates, hadoop_config_directory)
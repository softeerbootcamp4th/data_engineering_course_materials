import xml.etree.ElementTree as ET

# XML 파일 경로
core_site_xml_file_path = '../change-config/core-site.xml'
hdfs_site_xml_file_path = '../change-config/hdfs-site.xml'
mapred_site_xml_file_path = '../change-config/mapred-site.xml'
yarn_site_xml_file_path = '../change-config/yarn-site.xml'

# XML 파일 읽기
tree = ET.parse(core_site_xml_file_path)
root = tree.getroot()

# core-site 검증 파일 생성
with open('verify_core-site_conf.sh', 'w') as script_file:
    script_file.write("#!/bin/bash\n\n")

    script_file.write("check_conf() {\n")
    script_file.write("  local key=$1\n")
    script_file.write("  local expected_value=$2\n")
    script_file.write("  local actual_value=$(hdfs getconf -confKey $key 2>/dev/null)\n\n")
    script_file.write("  if [ \"$actual_value\" == \"$expected_value\" ]; then\n")
    script_file.write("    echo \"PASS: ['hdfs', 'getconf', '-confKey', '$key'] -> $actual_value\"\n")
    script_file.write("  else\n")
    script_file.write("    echo \"FAIL: ['hdfs', 'getconf', '-confKey', '$key'] -> $actual_value (expected $expected_value)\"\n")
    script_file.write("  fi\n")
    script_file.write("}\n\n")

    for property in root.findall('property'):
        name = property.find('name').text
        value = property.find('value').text
        script_file.write(f"check_conf {name} {value}\n")

print("Verification script has been created: verify_hadoop_conf.sh")

# hdfs-site 검증 파일 생성
with open('verify_hdfs-site_conf.sh', 'w') as script_file:
    script_file.write("#!/bin/bash\n\n")

    script_file.write("check_conf() {\n")
    script_file.write("  local key=$1\n")
    script_file.write("  local expected_value=$2\n")
    script_file.write("  local actual_value=$(hdfs getconf -confKey $key 2>/dev/null)\n\n")
    script_file.write("  if [ \"$actual_value\" == \"$expected_value\" ]; then\n")
    script_file.write("    echo \"PASS: ['hdfs', 'getconf', '-confKey', '$key'] -> $actual_value\"\n")
    script_file.write("  else\n")
    script_file.write("    echo \"FAIL: ['hdfs', 'getconf', '-confKey', '$key'] -> $actual_value (expected $expected_value)\"\n")
    script_file.write("  fi\n")
    script_file.write("}\n\n")

    tree = ET.parse(hdfs_site_xml_file_path)
    root = tree.getroot()

    for property in root.findall('property'):
        name = property.find('name').text
        value = property.find('value').text
        script_file.write(f"check_conf {name} {value}\n")
        
# mapred-site 검증 파일 생성
with open('verify_mapred-site_conf.sh', 'w') as script_file:
    script_file.write("#!/bin/bash\n\n")

    script_file.write("check_conf() {\n")
    script_file.write("  local key=$1\n")
    script_file.write("  local expected_value=$2\n")
    script_file.write("  local actual_value=$(hdfs getconf -confKey $key 2>/dev/null)\n\n")
    script_file.write("  if [ \"$actual_value\" == \"$expected_value\" ]; then\n")
    script_file.write("    echo \"PASS: ['hadoop', 'getconf', '-confKey', '$key'] -> $actual_value\"\n")
    script_file.write("  else\n")
    script_file.write("    echo \"FAIL: ['hadoop', 'getconf', '-confKey', '$key'] -> $actual_value (expected $expected_value)\"\n")
    script_file.write("  fi\n")
    script_file.write("}\n\n")

    tree = ET.parse(mapred_site_xml_file_path)
    root = tree.getroot()

    for property in root.findall('property'):
        name = property.find('name').text
        value = property.find('value').text
        script_file.write(f"check_conf {name} {value}\n")
        
        
# yarn-site 검증 파일 생성
with open('verify_yarn-site_conf.sh', 'w') as script_file:
    script_file.write("#!/bin/bash\n\n")

    script_file.write("check_conf() {\n")
    script_file.write("  local key=$1\n")
    script_file.write("  local expected_value=$2\n")
    script_file.write("  local actual_value=$(hdfs getconf -confKey $key 2>/dev/null)\n\n")
    script_file.write("  if [ \"$actual_value\" == \"$expected_value\" ]; then\n")
    script_file.write("    echo \"PASS: ['yarn', 'getconf', '-confKey', '$key'] -> $actual_value\"\n")
    script_file.write("  else\n")
    script_file.write("    echo \"FAIL: ['yarn', 'getconf', '-confKey', '$key'] -> $actual_value (expected $expected_value)\"\n")
    script_file.write("  fi\n")
    script_file.write("}\n\n")

    tree = ET.parse(yarn_site_xml_file_path)
    root = tree.getroot()

    for property in root.findall('property'):
        name = property.find('name').text
        value = property.find('value').text
        script_file.write(f"check_conf {name} {value}\n")

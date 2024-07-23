import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"ERROR: {e.output.strip()}"
    

def main():

    ##### ##### verify configs    
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
    expected_config = {
        "fs.defaultFS": "hdfs://hadoop-master:9000",
        "hadoop.tmp.dir": "file:///usr/local/hadoop/tmp",
        "io.file.buffer.size": "131072",
        "dfs.replication": "2",
        "dfs.blocksize": "134217728",  # 128 MB
        "dfs.namenode.name.dir": "file:///usr/local/hadoop/dfs/name",
        "mapreduce.framework.name": "yarn",
        "mapreduce.jobhistory.address": "hadoop-master:10020",
        "mapreduce.task.io.sort.mb": "256",
        "yarn.resourcemanager.address": "hadoop-master:8032",
        "yarn.nodemanager.resource.memory-mb": "8192",
        "yarn.scheduler.minimum-allocation-mb": "1024"
    }

    for config_key, expected_value in expected_config.items():
        command = ['/usr/local/hadoop/bin/hdfs', 'getconf', '-confKey', config_key]
        actual_value = run_command(command)
        if actual_value == expected_value:
            print('PASS:', end=' ')
            print(command, end=' ')
            print(f'-> {actual_value}')
        else:
            print('FAIL:', end=' ')
            print(command, end=' ')
            print(f'-> {actual_value} (expected {expected_value})')

    ##### ##### create testfile
    


if __name__ == "__main__":
    main()
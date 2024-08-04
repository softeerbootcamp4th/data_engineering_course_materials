import docker

command_set = [['hdfs', 'getconf', '-confKey', 'fs.defaultFS'],
               ['hdfs', 'getconf', '-confKey', 'hadoop.tmp.dir'],
               ['hdfs', 'getconf', '-confKey', 'io.file.buffer.size'],
               ['hdfs', 'getconf', '-confKey', 'dfs.replication'],
               ['hdfs', 'getconf', '-confKey', 'dfs.blocksize'],
               ['hdfs', 'getconf', '-confKey', 'dfs.namenode.name.dir'],
               ['hdfs', 'getconf', '-confKey', 'mapreduce.framework.name'],
               ['hdfs', 'getconf', '-confKey', 'mapreduce.jobhistory.address'],
               ['hdfs', 'getconf', '-confKey', 'mapreduce.task.io.sort.mb'],
               ['hdfs', 'getconf', '-confKey', 'yarn.resourcemanager.address'],
               ['hdfs', 'getconf', '-confKey', 'yarn.nodemanager.resource.memory-mb'],
               ['hdfs', 'getconf', '-confKey', 'yarn.scheduler.minimum-allocation-mb']]

outputs = ["hdfs://master:9000/",
           "/hadoop/tmp",
           "131072",
           "2",
           "134217728",
           "/hadoop/dfs/name",
           "yarn",
           "master:10020",
           "256",
           "master:8032",
           "8192",
           "1024"]


def mapreduce_wordcount():
    container.exec_run("hadoop fs -mkdir -p /tmp/test/wordcount")
    container.exec_run("hadoop fs -put /opt/hadoop/LICENSE.txt /tmp/test/wordcount")
    result = container.exec_run("hdfs dfs -stat %r /tmp/test/wordcount/LICENSE.txt")
    print("replication for file: ", result.output.decode("utf-8"))
    result = container.exec_run(
        "hadoop jar /opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar wordcount "
        "/tmp/test/wordcount /tmp/test/wordcount_out")
    for line in result.output.splitlines():
        print(line.decode("utf-8"))


def get_datanode_info():
    result = container.exec_run("yarn node -all -list -showDetails")
    for line in result.output.splitlines():
        print(line.decode("utf-8"))
    result = container.exec_run("yarn application -list -appStates ALL")
    for line in result.output.splitlines():
        print(line.decode("utf-8"))


def verify_configs():
    for command, expected in zip(command_set, outputs):
        result = container.exec_run(" ".join(command))
        output = result.output.splitlines()[0].decode("utf-8")
        if expected == output:
            print(f"[PASS]: {command} -> {output}")
        else:
            print(f"[FAIL]: {command} -> {output} (expected {expected})")


if __name__ == "__main__":
    client = docker.from_env()
    for container in client.containers.list():
        if container.image.tags[0] not in ['master:latest']:
            continue
        verify_configs()
        mapreduce_wordcount()
        get_datanode_info()

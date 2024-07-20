import subprocess


def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {' '.join(command)}")
        print(f"Error message: {error.decode('utf-8')}")
        return None
    return output.decode('utf-8').strip()


def verify_setting(command, expected_value):
    output = run_command(command)
    if output is not None:
        if output == expected_value:
            print(f"PASS: {command} -> {output}")
            return True
        else:
            print(f"FAIL: {command} -> {output} (Expected: {expected_value})")
    return False


def verify_replication_factor():
    test_file = "/tmp/test_file.txt"
    hdfs_path = "/test_file.txt"
    
    with open(test_file, 'w') as f:
        f.write("This is a test file for Hadoop verification.")
    
    run_command(['bin/hdfs', 'dfs', '-put', test_file, hdfs_path])
    
    command = ['bin/hdfs', 'fsck', hdfs_path, '-files', '-blocks', '-locations']
    output = run_command(command)
    if output:
        replication = output.split("replication=")[1].split()[0][:-1]
        if replication == "2":
            print(f"PASS: Replication factor is {replication}")

            run_command(['bin/hdfs', 'dfs', '-rm', '-f', hdfs_path])
            run_command(['rm', '-f', test_file])
            
            return True
        else:
            print(f"FAIL: Replication factor is {replication} (Expected: 2)")

    run_command(['bin/hdfs', 'dfs', '-rm', '-f', hdfs_path])
    run_command(['rm', '-f', test_file])
    
    return False


def main():
    settings = {
        ('bin/hdfs', 'getconf', '-confKey', 'fs.defaultFS'): 'hdfs://namenode:9000',
        ('bin/hdfs', 'getconf', '-confKey', 'hadoop.tmp.dir'): '/hadoop/tmp',
        ('bin/hdfs', 'getconf', '-confKey', 'io.file.buffer.size'): '131072',
        ('bin/hdfs', 'getconf', '-confKey', 'dfs.replication'): '2',
        ('bin/hdfs', 'getconf', '-confKey', 'dfs.blocksize'): '134217728',
        ('bin/hdfs', 'getconf', '-confKey', 'dfs.namenode.name.dir'): '/hadoop/dfs/name',
        ('bin/hdfs', 'getconf', '-confKey', 'mapreduce.framework.name'): 'yarn',
        ('bin/hdfs', 'getconf', '-confKey', 'mapreduce.jobtracker.address'): 'namenode:9001',
        ('bin/hdfs', 'getconf', '-confKey', 'mapreduce.task.io.sort.mb'): '256',
        ('bin/hdfs', 'getconf', '-confKey', 'yarn.resourcemanager.address'): 'namenode:8032',
        ('bin/hdfs', 'getconf', '-confKey', 'yarn.nodemanager.resource.memory-mb'): '8192',
        ('bin/hdfs', 'getconf', '-confKey', 'yarn.scheduler.minimum-allocation-mb'): '1024',
    }

    for command, expected_value in settings.items():
        verify_setting(command, expected_value)

    verify_replication_factor()


if __name__ == "__main__":
    main()
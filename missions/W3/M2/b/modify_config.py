import docker
import tarfile
import io
import os
import sys

if __name__ == "__main__":

    config_path = sys.argv[1]

    if len(sys.argv) != 2:
        print("Insufficient arguments")
        sys.exit()

    client = docker.from_env()
    print(f"Stopping Hadoop DFS....")
    print(f"Stopping YARN...")
    for container in client.containers.list():
        if container.image.tags[0] not in ['worker:latest', 'master:latest']:
            continue
        if container.image.tags[0] == 'worker:latest':
            result = container.exec_run('hdfs --daemon stop datanode')
            result = container.exec_run('yarn --daemon stop nodemanager')
        else:
            result = container.exec_run('hdfs --daemon stop namenode')
            result = container.exec_run('yarn --daemon stop resourcemanager')
    for config_file in ["core-site.xml", "hdfs-site.xml", "mapred-site.xml", "yarn-site.xml"]:
        for container in client.containers.list():
            print(f"Backing up {config_file}... in {container.name}")
            if container.image.tags[0] not in ['worker:latest', 'master:latest']:
                continue
            src_path = f"/etc/hadoop/{config_file}"
            dest_path = f"./backup/{container.name}/"
            # Get the tar stream of the file
            bits, stat = container.get_archive(src_path)
            # Read the tar stream and extract the file
            file_like_object = io.BytesIO()
            for chunk in bits:
                file_like_object.write(chunk)
            file_like_object.seek(0)
            with tarfile.open(fileobj=file_like_object) as tar:
                # Extract the file to the destination path
                member = tar.getmembers()[0]
                tar.extract(member, dest_path)

        for container in client.containers.list():
            print(f"Modifying {config_file}... in {container.name}")
            if container.image.tags[0] not in ['worker:latest', 'master:latest']:
                continue
            # 대상 파일 및 컨테이너 설정
            source_file_path = os.path.join(f"{config_path}/{config_file}")
            destination_path = os.path.join(f"/etc/hadoop/")
            # tar 파일 객체 생성
            obj_stream = io.BytesIO()
            with tarfile.open(fileobj=obj_stream, mode='w|') as tmp_tar, open(source_file_path, 'rb') as tmp_file:
                obj_info = tmp_tar.gettarinfo(fileobj=tmp_file)
                obj_info.name = os.path.basename(source_file_path)
                tmp_tar.addfile(obj_info, tmp_file)
            container.put_archive(destination_path, obj_stream.getvalue())

    print(f"Start Hadoop DFS....")
    print(f"Start YARN...")
    for container in client.containers.list():
        if container.image.tags[0] not in ['worker:latest', 'master:latest']:
            continue
        if container.image.tags[0] == 'worker:latest':
            # 스크립트 실행
            result = container.exec_run('hdfs --daemon start datanode')
            result = container.exec_run('yarn --daemon start nodemanager')
        else:
            result = container.exec_run('hdfs namenode -format')
            result = container.exec_run('hdfs --daemon start namenode')
            result = container.exec_run('yarn --daemon start resourcemanager')

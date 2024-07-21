# 인자를 2개만 받는다. 이때 첫 번째 인자는 HADOOP_HOME, 두 번째 인자는 CONTAINER_NAME이다. 세번재 인자는 없다
# 단 Container_name은 namenode에 대한 컨테이너 이름이다.
if [ $# -ne 2 ]; then
  echo "Usage: $0 <HADOOP_HOME> <CONTAINER_NAME>"
  exit 1
fi

HADOOP_HOME=$1
CONTAINER_NAME=$2

# 함수 정의: 디렉토리 생성
create_directory() {
  local dir=$1
  echo "Creating directory $dir..."
  docker exec -it $CONTAINER_NAME bash -c "
    if [ ! -d $dir ]; then
      mkdir -p $dir
    fi"
  if [ $? -ne 0 ]; then
    echo "Failed to create directory $dir inside the container."
    exit 1
  fi  
}

# 함수 정의: 파일 복사
copy_file() {
  local src_file=$1
  local dest_dir=$2
  echo "Copying $src_file..."
  docker cp $src_file $CONTAINER_NAME:$dest_dir/
  if [ $? -ne 0 ]; then
    echo "Failed to copy $src_file."
    exit 1
  fi
}

# mapreduce를 위한 디렉토리 생성
create_directory $HADOOP_HOME/mapreduce_test

# mapreduce를 위한 파일 복사
copy_file input.txt $HADOOP_HOME/mapreduce_test
copy_file wordcount.sh $HADOOP_HOME/mapreduce_test
########## 이곳에 파일을 추가하세요 ##########
# copy_file <SOURCE_FILE> $HADOOP_HOME/mapreduce_test
# end ##################################

# 복사한 파일들을 도커 컨테이너 내부에서 실행할 수 있도록 권한을 변경한다.
# 추가한 파일들에 대해서도 권한을 변경해야 한다.
docker exec -it $CONTAINER_NAME bash -c "
  sudo chown hadoop:hadoop $HADOOP_HOME/mapreduce_test/* &&
  chmod +x $HADOOP_HOME/mapreduce_test/input.txt
  chmod +x $HADOOP_HOME/mapreduce_test/wordcount.sh
  "

if [ $? -ne 0 ]; then
    echo "Failed to change permission of mapreduce test files inside the container."
    exit 1
fi

# wordcount.sh 실행
docker exec -it $CONTAINER_NAME bash -c "
  cd $HADOOP_HOME/mapreduce_test &&
  ./wordcount.sh
  "

if [ $? -ne 0 ]; then
    echo "Failed to run wordcount.sh inside the container."
    exit 1 
fi

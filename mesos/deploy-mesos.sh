zk(){
docker run --name zookeeper \
  --restart always \
  -d \
  --net=host \
  zookeeper
}

master(){
docker run -d --net=host \
  --name mesos_master \
  -e MESOS_PORT=5050 \
  -e MESOS_ZK=zk://192.168.136.186:2181/mesos \
  -e MESOS_QUORUM=1 \
  -e MESOS_REGISTRY=in_memory \
  -e MESOS_LOG_DIR=/var/log/mesos \
  -e MESOS_WORK_DIR=/var/tmp/mesos \
  -v "$(pwd)/log/mesos:/var/log/mesos" \
  -v "$(pwd)/tmp/mesos:/var/tmp/mesos" \
  mesosphere/mesos-master:1.7.0 \
  --ip=192.168.136.186 \
  --advertise_ip=192.168.136.186
}

slave(){
docker run -d --net=host --privileged \
  --pid=host \
  --cpus=0.5 \
  --memory=128M \
  --name mesos_slave \
  -e MESOS_PORT=5051 \
  -e MESOS_MASTER=zk://192.168.136.186:2181/mesos \
  -e MESOS_SWITCH_USER=0 \
  -e MESOS_CONTAINERIZERS=docker,mesos \
  -e MESOS_LOG_DIR=/var/log/mesos \
  -e MESOS_WORK_DIR=/var/tmp/mesos \
  -v "$(pwd)/log/mesos:/var/log/mesos" \
  -v "$(pwd)/tmp/mesos:/var/tmp/mesos" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /sys/fs/cgroup:/cgroup \
  -v /sys:/sys \
  -v /usr/bin/docker:/usr/local/bin/docker \
  mesosphere/mesos-slave:1.7.0 \
  --ip=192.168.136.190 \
  --launcher=posix \
  --no-systemd_enable_support 
}

marathon(){
docker run -d --net=host --privileged \
  --name mesos_marathon \
  mesosphere/marathon:v1.7.50 \
  --master zk://192.168.136.186:2181/mesos \
  --zk zk://192.168.136.186:2181/marathon \
  --http_port 8080 \
  --http_address 192.168.136.186
}

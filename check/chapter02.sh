DATA_DIR=$(cd $(dirname $0)/../data; pwd)
hightemp=$DATA_DIR/hightemp.txt

task10 () {
	wc -l $DATA_DIR/hightemp.txt
}
task11 () {
	cat $hightemp | sed s/'\t'/' '/g
}
task11

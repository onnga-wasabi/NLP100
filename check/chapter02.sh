DATA_DIR=$(cd $(dirname $0)/../data; pwd)
hightemp=$DATA_DIR/hightemp.txt

task10 () {
	wc -l $DATA_DIR/hightemp.txt 
}

task11 () {
	cat $hightemp | sed s/$'\t'/' '/g
}

task12 () {
	echo col1:
	cat $hightemp | cut -d $'\t' -f 1
	echo 
	echo col2:
	cat $hightemp | cut -d $'\t' -f 2
}

task13 () {
	paste ../src/output/col1.txt ../src/output/col2.txt
}
task14 () {
	n=${1:-5}
	head -$n $hightemp
}

task15 () {
	n=${1:-5}
	tail -$n $hightemp
}

task16 () {
	n=${1:-4}
	filesize=`cat $hightemp | wc -l`
	n=`echo 'scale=3;' $filesize/$n + 0.9 | bc`
	n=`echo $n/1 | bc`
	split -l $n $hightemp out.
}

task17(){
	cut -d $'\t' -f 1 $hightemp | sort | uniq
	echo 'num of set:\c'
	echo $((`cut -d $'\t' -f 1 $hightemp | sort | uniq | wc -l`))

}

task18(){
	sort -t $'\t' -k 3 $hightemp
}

task19(){
	sort -t $'\t' -k 1 $hightemp | cut -d $'\t' -f 1 | uniq -c | sort -r | awk '{print $NF}'
}
task19

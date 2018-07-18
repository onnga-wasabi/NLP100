DATA_DIR=$(cd $(dirname $0)/../src/output/; pwd)
case_pattern=$DATA_DIR/case_pattern.txt
mining=$DATA_DIR/mining.txt

task45(){
	echo 全て=================
	sort $case_pattern | uniq -c | sort -r | head

	echo する=================
	sort $case_pattern | uniq -c | sort -r | grep する | head

	echo 見る=================
	sort $case_pattern | uniq -c | sort -r | grep 見る | head

	echo 与える===============
	sort $case_pattern | uniq -c | sort -r | grep 与える | head
}

task47(){
	echo 述語=================
	sort $mining | cut -d $'\t' -f 1 | sort | uniq -c | sort -r | head

	echo 述語 + 助詞==========
	sort $mining -t $'\t' -k 1 | cut -f 1,2 | uniq -c | sort -r | head
}
task47

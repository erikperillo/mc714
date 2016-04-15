#!/bin/sh
#bench.sh -- automation of sinalgo testing
#put this file in sinalgo root directory and then create some directory to 
#save the results.

info()
{
	echo "[run.sh] "$1""
}

uniq_fn()
{
	local dir=$1
	local pattern=$2
	local i=0

	while [[ -e "$dir/$pattern$i" ]]; do
		i=$((i + 1))
	done	

	echo "$dir/$pattern$i"
}

get_area()
{
	echo "$nodes*3.14159265*($radius^2)/$density" | bc -l
}

get_size_square()
{
	printf "%.*f\n" 0 $(echo "sqrt($(get_area))" | bc -l)
}

#radius of communication of node
radius=100
#directory to store test results
res_dir=./results
#project name
proj=PI
#path to configuration file
config_file=./src/projects/$proj/Config.xml
#amount of RAM to use in MB
mem=4096
#number of iterations
its=5
#command for sinalgo
sinalgo_cmd=./sinalgo.sh

mkdir -p $res_dir

for i in $(seq 1 $its); do
	info "iter $i"

		for density in 10 15 20 25 30; do
			for nodes in 512 1024 2048 4096 8192; do
				dim=$(get_size_square)

				res_file="d"$density"_n"$nodes
				res_file=$(uniq_fn $res_dir "$res_file")
				info "saving in $res_file ..."

				info "density=$density, nodes=$nodes" | tee $res_file
				sleep 1

				info "compiling ..."
				ant compile

				info "running ..."
				time $sinalgo_cmd -project $proj \
					-gen $nodes $proj:$proj"Node" Random \
					-batch \
					-overwrite \
					dimX=$dim \
					dimY=$dim \
					javaVMaxMem=$mem \
					2>&1 | tee -a $res_file
			done
		done
done

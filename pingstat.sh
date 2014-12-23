#!/bin/bash

# Riley Spahn
# 08/24/14

get_ping_stat () {
    if [[ -z "$1" || -z "$2" ]] ; then 
        return 1
    fi
    target=$1
    pings=$2
    epoch=$(date +%s)
    pstat=$(ping -c $pings $target -q | grep "^rtt" | cut -d" " -f4 | sed "s/\// /g")
    echo "$epoch $pstat"
    return 0
}


update_dats () {
    PINGS=5
    stat_file=$1
    if [[ -z "$stat_file" ]] ; then 
        return 1
    fi

    for line in $( cat $stat_file); do
        url=$(echo $line | cut -d"," -f1)
        outfile=$(echo $line | cut -d"," -f2)
        get_ping_stat $url $PINGS >> $outfile
    done
}

generate_figs () {
    out_dir=$1

    for dat_file in $( ls *.dat); do
        python generate_figures.py $dat_file $out_dir
    done
}

generate_html() {
    out_dir=$1
    index_file="$out_dir/index.html"
    tmp_file=".index.html.bak"

    echo "<html><title>Ping Stat</title><b>Ping Stat</b>" >> $tmp_file

    for img in $( ls $out_dir/*.png ); do
        img_file=$( echo $img | cut -d"/" -f2 )
        echo "<p><img src=\"$img_file\"/></p>" >> $tmp_file
    done
    echo "</html>" >> $tmp_file
    mv $tmp_file $index_file
}

out_dir="out"
mkdir -p $out_dir

# Ping all the things based on the input file
update_dats $1

# Generate the new figures.
generate_figs $out_dir

# Regenerate HTML.
generate_html out out/figs

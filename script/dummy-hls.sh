#!/bin/bash


if [ $# -ne 1 ]; then
  echo "Error: Please provide exactly one argument: path/to/file.mp4"
  exit 1
fi

input_file="$1"

if [ ! -f "$input_file" ]; then
  echo "Error: File '$input_file' does not exist."
  exit 1
fi

dir_path=$(dirname "$input_file")

mkdir -p "$dir_path/$(basename "$input_file" .mp4)"

if [ $? -ne 0 ]; then
  echo "Error: Failed to create directory '$dir_path'"
  exit 1
fi

# Generate the output filename (stream.m3u8)
output_file="$dir_path/$(basename "$input_file" .mp4)/stream.m3u8"

ffmpeg -i $1 -profile:v baseline -level 3.0 -start_number 0 -hls_time 10 -hls_list_size 0 -f hls $output_file
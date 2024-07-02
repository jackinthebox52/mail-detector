for f in *.webp; do ffmpeg -i "$f" "${f%.*}.png" && rm "$f"; done

for f in *.jpeg; do ffmpeg -i "$f" "${f%.*}.png" && rm "$f"; done

for f in *.jpg; do ffmpeg -i "$f" "${f%.*}.png" && rm "$f"; done

for f in *.avif; do ffmpeg -i "$f" "${f%.*}.png" && rm "$f"; done

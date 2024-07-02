counter=1
for f in *.png; do
  mv "$f" "$1-$counter.png"
  ((counter++))
done

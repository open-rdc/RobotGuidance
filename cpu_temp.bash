printf '%s\n' phy core0 core1 core2 core3 | paste -sd '\t' >> cpu_temp.csv
while true
do
phy=$(sensors | grep "Physical" | awk '{printf $4}' | sed "s/+//" | sed "s/°C//")
core0=$(sensors | grep "Core 0" | awk '{printf $3}' | sed "s/+//" | sed "s/°C//")
core1=$(sensors | grep "Core 1" | awk '{printf $3}' | sed "s/+//" | sed "s/°C//")
core2=$(sensors | grep "Core 2" | awk '{printf $3}' | sed "s/+//" | sed "s/°C//")
core3=$(sensors | grep "Core 3" | awk '{printf $3}' | sed "s/+//" | sed "s/°C//")
#echo -e "$phy\t$core0\t$core1\t$core2\t$core3"
printf '%s\n' $phy $core0 $core1 $core2 $core3 | paste -sd '\t' >> cpu_temp.csv
sleep 0.2s
done

conda activate westpa-2022.02

./init.sh
./run.sh
w_fluxanl
mv fluxanl.h5 flux_1.h5

./init.sh
./run.sh
w_fluxanl
mv fluxanl.h5 flux_2.h5

./init.sh
./run.sh
w_fluxanl
mv fluxanl.h5 flux_3.h5

./init.sh
./run.sh
w_fluxanl
mv fluxanl.h5 flux_4.h5

./init.sh
./run.sh
w_fluxanl
mv fluxanl.h5 flux_5.h5

./init.sh
./run.sh
w_fluxanl
mv fluxanl.h5 flux_6.h5

./init.sh
./run.sh
w_fluxanl
mv fluxanl.h5 flux_7.h5

./init.sh
./run.sh
w_fluxanl
mv fluxanl.h5 flux_8.h5

./init.sh
./run.sh
w_fluxanl
mv fluxanl.h5 flux_9.h5

./init.sh
./run.sh
w_fluxanl
mv fluxanl.h5 flux_10.h5

rm west.h5
mv *.h5 flux_analysis

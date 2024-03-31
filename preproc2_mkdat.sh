# Run only AFTER you have run preproc1_helo.sh and AFTER you have created the .par files
# Andrea: run as data user

# Command to run this file:
# cat parallel_process_args | xargs -n 2 -P 6 ./preproc2_mkdat.sh

# -P x: x is the max number of processes you allow to run at a time
# -n x: Tells xargs that it should read the argument file two whitespace separated entries at a time. 

#####################################################################################################
# Step 1: Change the animal ID below to the correct one. Make the parallel_process_args file (File format: whitespace-separated single line with the recording date in YYYYMMDD format and the total num of recordings for that day.)
animal="JC283"
diskorigin="adata1" # location of the .bin files
diskdest="adata2" #location the .dat files should go

rec_date=$1 #In BASH $1 refers to the first argument passed
num_sessions=$2 #In BASH $2 refers to the second argument passed

basename=$animal"-"$rec_date
processfold=$rec_date

cd /$diskorigin/data/$animal/$rec_date

echo $processfold
#Step 2: Run axona2dat3_15_128, mv the .dat and .axtrk files and copy the .set files to the correct processing folder

for i in `seq 5 $num_sessions`; #note: change 5 back to 1 #this will create a "010" session, but if I do `seq 1 9` it'll always make 9 files, need to find a way to fix it (Andrea 2022-06-12)
do
	Axona2dat3_15_128 $basename"_0"$i".bin"; #ideally I should check if the .bin file exists first, as sometimes it creates empty .dat files
	echo $i
done
	
#for i in `seq 10 $num_sessions`;
#do
#	Axona2dat3_15_128 $basename"_"$i".bin";
#	echo $i 
#done

#mv *.dat /$diskdest/processing/$animal/$processfold;
#mv *.axtrk /$diskdest/processing/$animal/$processfold;
#mv *.digbin /$diskdest/processing/$animal/$processfold; #commenting out because I don't use digbin
#rsync *[0-9].{dat,digbin,axtrk} /$diskdest/processing/$animal/$processfold #consolidating above 3 lines

#have to remove files afterwards

cd /$diskdest/processing/$animal/$processfold
rm $basename"_"0?"s."* #To delete any .set/.dat/.axtrk files associated to the screening/tuning recordings. 
#Note from Andrea on 2022-05-31: I'm commenting out for now because I don't want to delete these files. 20220612: deleting after all

#Step 3: Downsampling 
#echo $processfold ": Downsampling started"
#check_len_24_20_div16_resample2_JONb 128
#echo $processfold ": Downsampling done"

#Step 4: Create the whls
#echo $processfold ": Creating the whls"
#folder_make_axona_whl_JONb 128
#echo $processfold ": Done creating the whls"

#Step 5: Spike extraction --------> Assuming the .par and.parth files have already been created > step not needed for msort
#echo $processfold ": Spike extraction started"
#smprocnew-setthr $basename
#echo $processfold ": Spike extraction done"

echo $processfold ":DONE WITH EVERYTHING FOR THIS RECORDING DAY! :D"

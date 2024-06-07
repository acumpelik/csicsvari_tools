#!/bin/bash

animal='JC315'
rew_arms_file="$animal.reward_arms"
basenames_file=basenames_all_animals
path="/Users/andrea/adata_laptop/merged"

echo "Now generating reward arms files for $animal using $basenames_file as a list of recording sessions and $rew_armfile as a reward arms source file."

# Read the animal name and day from the basenames_file and copy the reward arms file twice for each day (training1 and 2).
while IFS=' ' read -r animal_id day; do
	if [[ "$animal_id" == "$animal" ]]; then
		target_file1="${animal_id}-${day}_training1.reward_arms"		
		target_file2="${animal_id}-${day}_training2.reward_arms"
		cp $rew_arms_file $target_file1
		cp $rew_arms_file $target_file2

		echo "Created files: $target_file1 and $target_file2"
		# Copy the files to their respective directory
		target_path="$path/$animal-$day"
		mv $target_file1 $target_path
		mv $target_file2 $target_path
		echo "Moved files to $target_path"

	fi
done < "$basenames_file"


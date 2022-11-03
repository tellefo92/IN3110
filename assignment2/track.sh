#!/bin/bash
FILE=~/.local/share/.timer_logfile
if [ ! -f $FILE ] #Check if .timer_logfile exists, creates a blank .timer_logfile if file is not found
	then
	touch ~/.local/share/.timer_logfile
	echo "File created"
fi
grep -q "LOGFILE" ~/.bashrc
if [ $? -eq 1 ] # Check if the LOGFILE variable is set in .bashrc
	then
	echo 'export LOGFILE="$HOME/.local/share/.timer_logfile"' >> ~/.bashrc # Adds environmental variable to .bashrc
fi
running=false # Variable to keep track of whether or not we're tracking a task
function track() {
	if [ $# -lt 1 ] # Just making sure the user uses the script correctly
		then
		echo "Choose one of the following options:"
		echo "track start [label]"
		echo "track stop"
		echo "track status"
		echo "track log"
	fi
	if [ $1 == "start" ] # What to do when user running 'track start [label]'
		then
			if [ "$running" == true ] # Returns error message if user attempts to track multiple tasks at once
				then
				echo "Already tracking task with $label"
			else
				running=true
				label_start=$(date +"%a %b %d %H:%M:%S CEST %Y") # Getting correct time format
				label=${@:2} # Fetching label from command line input
				echo "START $label_start" >> ~/.local/share/.timer_logfile # Adding start date and time to the .timer_logfile
				echo "LABEL $label" >> ~/.local/share/.timer_logfile # Adding label name to the .timer_logfile
				echo "Started tracking task with label $label"
			fi
	elif [ $1 == "stop" ] # What to do when user running 'track stop'
		then
			if [ "$running" == false ] # Check if a task is running or not
				then
				echo "No task currently being tracked."
			else
				running=false
				label_stop=$(date +"%a %b %d %H:%M:%S CEST %Y") # Getting correct time format
				echo "END $label_stop" >> ~/.local/share/.timer_logfile # Adding stop date and time to the .timer_logfile
				echo " " >> ~/.local/share/.timer_logfile # Adding whitespace to .timer_logfile for formatting purposes
				echo "Stopped tracking task with label $label"
			fi
	elif [ $1 == "status" ] # What to do when user running 'track status'
		then
		if [ "$running" == true ] # What to do if a task is currently being tracked
			then
			echo "Currently tracking task $label."
		else
			echo "No task currently being tracked."
		fi
	elif [ $1 == "log" ] # What to do when user running 'track log'
		then
			grep -E "^[A-Za-z0-9]" ~/.local/share/.timer_logfile | while read -r line # Find all lines of .timer_logfile containgin alphanumeric text, and parse all found lines
			do
				if [[ "$line" == START* ]] # Lines starting with the word START
					then
					time=$(echo "$line" | cut -d' ' -f 2-) # Getting all words on the line after the first word
					start=$(date -d"$time" +"%s") # Time formatting
				elif [[ "$line" == LABEL* ]] # Lines starting with the word LABEL
					then
					label=$(echo "$line" | cut -d' ' -f 2-) # Getting all words on the line after the first word
				elif [[ "$line" == END* ]] # Lines starting with the word END
					then
					time=$(echo "$line" | cut -d' ' -f 2-) # Getting all words on the line after the first word
					end=$(date -d"$time" +"%s") # Time formatting
					duration=$(($end-$start)) # Calculate duration
					if [ "$duration" -gt 86399 ] # Handling for durations over 24 hours
						then
						hours=$(($duration/3600))
						rem=$(($duration%3600))
						minutes=$(($rem/60))
						if [ "$minutes" -lt 10 ]
							then
							minutes="0$minutes" # Format handling
						fi
						seconds=$(($rem%60))
						if [ "$seconds" -lt 10 ]
							then
							seconds="0$seconds" # Format handling
						fi
						echo "Task $label: $hours:$minutes:$seconds"
					else
						hhmmss=$(date -d@$duration -u +"%H:%M:%S") # Time formatting
						echo "Task $label: $hhmmss"
					fi
				fi
			done
	else
		echo "Not a recognized option."
	fi
}

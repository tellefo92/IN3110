#!/bin/bash
source=$1
destination=$2
if [ ! -d $1 ] # Check that source directory exists
then
	echo "Directory /$1 doesn't exist."
fi
if [ ! -d $2 ] # Check if destination directory exists
then
echo "Directory /$2 does not exist. Would you like to create this directory? (Y/N):"
read response
if [ $response = "Y" ] || [ $response = "y" ] # Check if the user wants to make a new destination directory 
then 
	echo "Would you like the directory to:"
	echo "1) Be named $2?"
	echo "2) Be named with the current date and time in the format YYYY-MM-DD-hh-mm?"
	echo "3) Be named something else that you choose?"
	echo "Please respond with your option (1/2/3):"
	read response
	if [ $response = "1" ] # User wants directory to be named what they input
	then 
	mkdir $destination
	echo "Directory $destination created. Moving files."
	elif [ $response = "2" ] # User wants directory to be named with date and time
	then
	destination=$(date +"%Y-%m-%d-%H-%M") # Fetching date and time in correct format
	mkdir $destination # Create directory with date and time as name
	echo "Directory $destination created. Moving files."
	elif [ $response = "3" ] # User wants to name directory something else
	then
	echo "What would you like to name the folder?"
	read folder_name
	destination=folder_name
	mkdir $destination
	echo "Directory $destination created. Moving files."
	fi	
elif [ $response = "N" ] || [ $response = "n" ] # User does not want to make a new folder
then 
	echo "Ok. Stopping program. Please provide an existing directory when running the program."
	exit 9999
else
	echo "Not a valid response. Stopping program."
	exit 9999
fi
fi
if [ $# -lt 2 ] # Check that user supplies enough command line arguements
then
echo "Please specify the directory where files are to be moved from, and the directory where the files are to be moved to."
fi
if [ $# -gt 2 ] # Check that user did not supply too may arguements
then
echo "This script uses 2 commandline arguements, the first being the source directory, and the second being the destination directory. You provided $# arguements."
fi
echo "Would you like to move specific file types, or all types? Specify the file extension (i.e. .txt) or type all if you want all files and folders to be moved."
read response
if [ $response = "all" ]
then
mv $1/* $destination # Move all files and subdirectories from source to destination
echo "Moved all files from $1 to $destination."
else
mv $1/*$response $destination # Only move files with suffix specified by the user from source to destination
echo "Moved $response files from $1 to $destination."
fi

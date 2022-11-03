
# README.md Assignment2 

## Task 2.1

### Prerequisites

To make the script executable, run the following command in a bash-terminal:
```bash
chmod a+x ./move.sh
```
### Functionality

Moves files between directories chosen by the user.
If the user would like, they can move folders to a new directory named as the user wishes, including directories named the current date and time.

### Missing Functionality

Does not work in directories where the `move.sh` file is not located.

### Usage

To move files between folders `src` and `dst`, run the following command in a bash-terminal (in the directory where move.sh is located): 

```bash
./move.sh src dst
```

To move files between `src` and a `new_folder` to be named by the user, run the following command in a bash-terminal, and follow the instructions.

```bash
./move.sh src new_folder
```
## Task 2.2/2.3
### Prerequisites

The code is only tested on the IFI-machines at UIO.
The script automaticall sets the environment variable LOGFILE, so the user doesnt have to.
To make the script executable, the user needs to type the following into their terminal:
```bash
chmod a+x ./track.sh
```
and then type
```bash
source track.sh
```
and finally
```bash
source ~/.bashrc
```

### Functionality

Tracks time spent on a task, and logs the start time, label and end time of the task to a file called .timer_logfile, placed in the directory `~/.local/share`. 

To print the contents of the `.timer_logfile`, the user can use the command
```bash
cat $LOGFILE
```

### Missing Functionality

Can only track one task at a time.
Can't be used to check time spent on a task that is currently running.

### Usage

To start tracking a task use the command
```bash
track start [label] # [label] can be whatever the user wants it to be
```
To end tracking of a task use the command
```bash
track stop
```
To check if a task is running, and the label of a running task, use the command
```bash
track status
``` 
To check time spent on previously finished tasks, use the command 
```bash
track log
```

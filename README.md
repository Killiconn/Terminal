# Readme
This is a simple manual describing how to use my shell, all the commands and functions will be explained within.

quit    -  Leaves the shell.

dir     -  Lists all the files and directories within the directory in which you are in.
	<Arguments>
   	- h : Lists all the files and directories including hidden files, within the directory in which you are in.

clr     -  Clears the terminal shell screen.

cd      -  Changes the shells working directory.
	<Arguments>
	- arg : Changes the shells working directory to the file contains in arg
		If the args file is non existent, then an error will show
	- .. : navigate up one directory level
	- None : If no args are given, the current working directory goes to the previous directory.
	 	 
pwd     -  Prints the name of the current working directory.

environ -  This returns a list of environment variables. Which are dynamic values that affect processes or programs.
 
echo    -  Outputs arguments to standard output.

pause   -  Pause the shell until enter is pressed.

myshell -  Executes the contents of the file which is passed as the argument.
	   For Example: if the contents of a file was echo hello. The terminal will print hello.
        
python3 -  Runs Python3 in the shell.

view    -  Views the contents of the file which is passed as the argument.

help    -  Produces a menu of topics that you may need help with
	   <Arguments>
	   - arg : Any of the the command has a clear and helpfule decription of what the command does.

from __future__ import print_function
import cmd
import os, sys, shlex, subprocess, time

global old_cmd 

class MyPrompt(cmd.Cmd):

	def do_quit(self, args):
		'''Quits the program.'''
		if args:
			self.error_message("quit", args)
		else:	
			print ('Quitting.')
			raise SystemExit

	def do_dir(self, args):
		'''This functions lists the files and directories in the directory that you are in.
		It obtains the files from the current directory using the listdir functions.
		I have my code such that if you insert a "h" after the dir command it lists all
		the hidden files along with normal files.'''
		if not args:
			files = os.listdir(".")
			lst = []
			for name in files:
				if name[0] != ".":
					lst.append(name)
			lst = sorted(lst)
			for file in lst:
				print(file)

		else:
			if args[0] == "/":
				files = os.listdir("." + args)
			else:
				files = os.listdir(".")
			
			lst = []
			hiddenlst = []
			for name in files:
				if name[0] != ".":
					lst.append(name)
					hiddenlst.append(name)
				else:
					lst.append(name)

			if args.split()[0] == "h":		#hidden files
				for name in hiddenlst:
					print(name)

			elif args[0] == "/":
				for file in lst:
					print(file)

			else:
				self.error_message("dir", args)


	def do_clr(self, args):				
		'''Clears the screen '''
		sys.stdout.write("\033c")
	
	def do_cd(self, args):
		'''CD is a change directory command. Firstly you obtain the current diectory using 
		the get current working directory command in the os library.
		My code is very simple, first you see if there is arguments then you append the arguments
		of the function to the directory you are in. Thats it. This also works for when you have a file within
		a file situation. If the file is not there, the terminal will throw a file not found error.
		This will be caught and an appropriate error message will appear'''
		try:
			directory = os.getcwd()
			if len(args) > 0:
				directory = directory + "/" + args		
				os.chdir(directory)

			elif args == "":
				files = directory.split("/")
				directory = "/".join(files[:4])
				os.chdir(directory)
		
		#If the directory is non exsistant than it throughs an error
		except (FileNotFoundError, NotADirectoryError):
			print("bash: cd: " + args + ": No such directory")

	def do_pwd(self,args):
		'''The getcwd gets the current working directory'''
		print(os.getcwd())

	def do_environ(self, args):
		'''This command is used to print a list of environment variables. Theses are dynamic values which affect the processes or
		programs on a computer. When environ is entered it prints them all.'''
		lst = []
		arguments = args.split()
		for key in os.environ:
			lst.append(key + "=" + os.environ[key])	
		if len(arguments) == 0:
			for item in lst:
				print(item)
		else:
			self.error_message("environ", args)

	def do_echo(self, args):
		'''Echo is a print statement function. The reason for my stringcondition boolean value is because if you type a string with an odd number
		of quotation marks, the terminal thinks that you are not finished. Within the shlex.split() function is expects an even number of
		quotations, otherwise it will throw a ValueError. I have caught this and asks for another input and append it to the previous arguments.
		Newline character will also be printed just like the echo command in any other terminal.'''
		stringcondition = True
		while stringcondition:
			try:
				print(" ".join(shlex.split(args)))
			except IndexError:
				#No arguments given returning nothing
				print("")
			except ValueError:
				sys.stdout.write(">")
				inp = input()
				args += "\n" + inp
			else:
				stringcondition = False

	def do_pause(self, args):
		'''This command pauses the shell until paused is pressed'''
		'''If arguements are given throw an error'''
		if args:
			self.error_message("pause", args)
		else:	
			print("Pausing until enter is pressed.")
			n = input()
			if n == "":
				print("Enter was pressed")
			else:
				self.do_pause(args)

	def do_myshell(self, batchfile):
		'''This goes into any file which is called and executes the contents of that file in
		the terminal. If the file or directory is not found it throws an appropriate error.
		The "onecmd" command that is used bellow, interprets the argument as though it had been 
		typed in response to the prompt.'''
		try:
			batchfile = batchfile.strip()
			file = open(os.getcwd() + "/" + batchfile, "r")
			text = file.readlines()
			for item in text:
				item = item.strip()
				self.onecmd(item)
		except:
			print("Can't open file '"+ batchfile + "': No such file or directory")


	def precmd(self, lines):
		'''This is another cmd tool that allows to execute something before the command line
		is interpreted but after the input is generated and issued. I used this tool the catch any
		redirections in the command line. If there is redirecting i want to open/create the file
		name and get the normal standard output into/append it to the file.'''
		line = lines.split()
		redir = [">",">>"]
		red_cmd = ["help", "dir", "echo", "environ"]
		ind = [i for i in range(len(line)) if line[i] in redir]
		try:
			if line[0] in red_cmd and len(ind):
				if line[ind[0]] == redir[0]:
					sys.stdout = open(line[ind[0]+1], "w+")

				elif line[ind[0]] == redir[1]:
					sys.stdout = open(line[ind[0]+1], "a")

				return " ".join(line[:ind[0]] + line[ind[0] + 2:])
			else:
				return lines
		except:
			return lines

	def emptyline(self):
		'''This function basically get rid of repitition, without this the terminal will remember the
		last command entered and will execute it again if an emptyline was entered. This just passes it
		and executes nothing.'''
		pass
    
	def postcmd(self, stop, line):
		sys.stdout = sys.__stdout__
		self.prompt = "~" + os.getcwd() + " $ "
	
	def do_python3(self, arg):
		'''If you would like to use python in the terminal shell, The reasons for the wait, is because
		without it the terminal will be fighting for input. This is an example of zombie process, this is a 
		process that has completely executed but still has an entry in the process table.'''
		if len(arg) >= 1:
			p = subprocess.Popen(["python3", arg])
			p.wait()
		else:
			p = subprocess.Popen(["python"])
			p.wait()

	def do_view(self, arg):
		'''This is just a handy view function that lets me see what is inside any files.'''
		try:	
			file = arg.strip()
			file = open(file, "r")
			text = file.readlines()
			#self.do_clr(arg)
			i = 0
			while i < len(text): 
				print(text[i].strip())
				if i % 25 == 0:
					input("~~~~~~~~~~~~~~~~Press Enter for more~~~~~~~~~~~~~~~~~~~")
				i = i + 1

		except FileNotFoundError:
			print("No such file or directory: " + arg)



	def error_message(self, comd, arg):
		'''This is an error message function.'''
		command = ["environ", "pause", "dir"]
		if comd in command:
			print(comd + ": invalid option -- '" + arg + "'")
		elif comd == "quit":
			print("SyntaxError: invalid syntax")

	
	def help_help(self):
		'''All helpfiles'''
		print('''
This is a simple manual describing how to use my shell, all the commands and functions will be explained within.
help    -  Produces a menu of topics that you may need help with
	   <Arguments>
	   - arg : Any of the the command has a clear and helpfule decription of what the command does.
		   Also, the decription of the topics below are given.
			''')
		#helps = [self.help_quit(),self.help_dir(),self.help_clr(),self.help_cd(),self.help_pwd(),self.help_environ(),self.help_echo(),self.help_pause(),self.help_myshell(),self.help_python3(),self.help_view(),self.help_Redirection(),self.help_Background(),self.help_EnvironmentConcepts()]
		self.do_view("readme")

	def help_quit(self):
		print("""
quit    -  Leaves the shell.""")

	def help_dir(self):
		print('''
dir     -  Lists all the files and directories within the directory in which you are in.
	<Arguments>
	- h : Lists all the files and directories including hidden files, within the directory in which you are in.
   			''')

	def help_clr(self):
		print('''
clr     -  Clears the terminal shell screen.
			''')

	def help_cd(self):
		print('''
cd      -  Changes the shells working directory.
	<Arguments>
	- arg : Changes the shells working directory to the file contains in arg
		    If the args file is non existent, then an error will show
	- .. : navigate up one directory level
	- None : If no args are given, the current working directory goes to the previous directory.
			''')

	def help_pwd(self):
		print('''
pwd     -  Prints the name of the current working directory.
			''')

	def help_environ(self):
		print('''
environ -  This returns a list of environment variables. Which are dynamic values that affect processes or programs.
			''')

	def help_echo(self):
		print('''
echo    -  Outputs arguments to standard output.
			''')
	def help_pause(self):
		print('''
pause   -  Pause the shell until enter is pressed.
			''')

	def help_myshell(self):
		print('''
myshell -  Executes the contents of the file which is passed as the argument.
		   For Example: if the contents of a file was echo hello. The terminal will print hello.
			''')

	def help_python3(self):
		print('''
python3 -  Runs Python3 in the shell.
			''')

	def help_view(self):
		print('''
view    -  Views the contents of the file which is passed as the argument.
			''')

	def help_Redirection(self):
		print('''
Redirection:
	A pipe is a form of redirection where you transfer of standard output to some other destination. I.E a file. 
	In this terminal the following commands can do redirecting: echo, help, dir and environ.
	There is two types of redirecting in this terminal:
		1) When used like this: "dir > newfile" the contents of dir is printed in the user-specified location(newfile) , whether it 			   
		exists or not. If it is prexistant, then contents is overwritten and is saved.
		2) When used like this: "dir >> newfile" the contents of dir once again is printed in the newfile, however,
		   If the file is already existing, then the contents is appended onto user-specified file.

			''')

	def help_EnvironmentConcepts(self):
		print('''
Environment Concepts:
	Environment is the state of the computer, it is usually determined by which programs are being run and hardware and
	software characteristics. Environment variables are values that are placeholders for information. It then passes
	data to programs that are launched in shells or subshells. Some examples of these variables include the name of 
	shell programs, home directories, language and of course the current working directory.

			''')

	def help_Background(self):
		print('''
Background Processes:
	This is computer process, only it runs behind the scenes without bothering the user. This is usually used for 
	processes that take a longer period of time that others. Due to this time period, the user may wish to do 
	something else, concurrently. It is represented by a symbol & at the end of the command.	
	This terminal shell however doesn't allow background executions as I was unable to get them working. I tried using fork
	and exec functions as its own child processes. Daemonizing and starting threads was also attempted. Daemon threads are
	essential for background processes.
			''')

if __name__ == '__main__':
	'''This old_cmd variable is for the help file, as soon as you run the program, it is 
	assumed that the helpfile is in the same directory as myshell.py, and the current 
	working directory is saved.'''
	old_cmd = os.getcwd()
	prompt = MyPrompt()
	prompt.prompt = "~" + os.getcwd() + " $ "  
	if len(sys.argv) == 1:
		prompt.cmdloop('Starting prompt...')
	else:
		prompt.do_myshell(sys.argv[1])
		prompt.do_quit("")

# Flet Windows Optimizer
This is an application developed with Flet that includes some functions to optimize Windows. At the moment it only has 3 buttons to delete temporary files, but it could be extended in the near future.

## How to use it
It's a pretty straightforward program to use, but you can do some extra things depending on the context.
- If the program shows some strange behavior (like not deleting any files), you can try to run it via CMD. This will print out any Python exception, so you can open an issue in this repository with that information and I will take a look at it.
- In order to run some commands, the program needs to be run as an administrator. This is only because Python by default does not have permission to access directories outside your current user, so it can't clean up `C:\Windows\Temp` or `C:\Windows\Prefetch`. The program has a pop-up to remind you of this anyway.

Any advice to implement more features is obviously welcome!
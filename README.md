# free dog sdk

This should be a free version of the robodog go1 sdk. I was upset that the original sdk only comes in precompiled libs, so i started to write this. It is far from finished but it can be used to send highLevelCmds to the dog.
LowLevelCmds are not yet fully implemented, also reading back the status messages isn't done, aswell as the proper threading for the socket communication is not done.
Any help is welcome.
See speak.py for a minimum example, it lets the dog rotate 90Degree left via HighLevel Command. Connect to Dogs wifi and run it.

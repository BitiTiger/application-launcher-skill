# needed to make a mycroft skill
from mycroft import MycroftSkill, intent_file_handler
# needed to check if operating system is Linux
from sys import platform
# needed to run program as subprocess
import subprocess


class ApplicationLauncher(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('launcher.application.intent')
    def handle_launcher_application(self, message):
        # check if the user is an idiot
        if not platform.startswith('linux'):
            self.speak_dialog("I can only launch programs on Linux systems.")
            return
        # check that program was understood
        if not 'program' in message.data:
            self.speak_dialog(
                "I did not understand the program name. Try asking again.")
            return
        # execute specified program
        self.runProgram(message.data['program'])

    def runProgram(self, program):
        # run program as subprocess
        # NOTE:  the program is assumed to be an executable in the user's $PATH environment variable
        try:
            # attempt to run directly
            subprocess.Popen(program, stderr=subprocess.DEVNULL)
            self.speak_dialog("Launched program.")
        except:
            # determine if program name is longer than one word
            if len(program.split()) > 1:
                # chop program
                program = program.split()
                
                # program name may be hyphenated
                progName = ""
                for p in program:
                    progName += p
                    progName += '-'
                progName = progName[:len(progName)-1]
                try:
                    subprocess.Popen(progName, stderr=subprocess.DEVNULL)
                    self.speak_dialog("Launched program.")
                    return
                except:
                    pass

                # program name may use underscores
                progName = ""
                for p in program:
                    progName += p
                    progName += '_'
                progName = progName[:len(progName)-1]
                try:
                    subprocess.Popen(progName, stderr=subprocess.DEVNULL)
                    self.speak_dialog("Launched program.")
                    return
                except:
                    pass

                # program name may accidentally have spaces when it is just one word
                progName = ""
                for p in program:
                    progName += p
                try:
                    subprocess.Popen(progName, stderr=subprocess.DEVNULL)
                    self.speak_dialog("Launched program.")
                    return
                except:
                    pass
            self.speak_dialog("I do not know a program by that name.")


def create_skill():
    return ApplicationLauncher()

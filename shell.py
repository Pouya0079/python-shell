import os
import subprocess as sp

from pyfiglet import Figlet


class Shell:
    """Simple Shell Implemented in Python3.6"""

    def __str__(self):
        return f'\033[1;34;40m{self.__class__.__doc__}'

    @staticmethod
    def set_screen():
        """Set color screen and clear it"""

        print('\033[1;32;40m')
        os.system('clear')

    @staticmethod
    def shell_figlet():
        """Set a figlet text for shell"""

        fgl = Figlet(font='slant')
        print(fgl.renderText('Python Shell'))

    @staticmethod
    def execute_pipe_command(command):
        """Method for executing pipe commands"""

        tmp_in, tmp_out = (0, 0)
        tmp_in = os.dup(0)
        tmp_out = os.dup(1)

        fdin = os.dup(tmp_in)

        for cmd in command.split('|'):
            os.dup2(fdin, 0)
            os.close(fdin)

            if cmd == command.split('|')[-1]:
                fdout = os.dup(tmp_out)

            else:
                fdin, fdout = os.pipe()

            os.dup2(fdout, 1)
            os.close(fdout)

            try:
                sp.run(cmd.strip().split())

            except Exception:
                print(f'\033[1;31;40mError: command not found: {cmd}')

        os.dup2(tmp_in, 0)
        os.dup2(tmp_out, 1)
        os.close(tmp_in)
        os.close(tmp_out)

    @staticmethod
    def change_directory(path):
        """Method for changing directories"""

        try:
            os.chdir(os.path.abspath(path))

        except Exception:
            print(f'\033[1;31;40mError: no such file or directory: {path}')

    def execute_command(self, command):
        """Method for executing commands using subprocess"""

        try:
            if '|' in command:
                self.execute_pipe_command(command)

            else:
                sp.run(command.split())

        except Exception:
            print(f'\033[1;31;40mError: command not found: {command}')

    def main(self):
        """Main function for controling operations"""

        self.set_screen()
        self.shell_figlet()

        while True:
            cwd = os.getcwd().split('/')[-1]
            command = input(f'\033[1;32;40m({cwd}): ~ ')

            if command == 'exit':
                break

            elif command == 'help':
                print(self.__str__())

            elif command[:3] == 'cd ':
                self.change_directory(command[3:])

            else:
               self.execute_command(command)


if __name__ == "__main__":
    Shell().main()

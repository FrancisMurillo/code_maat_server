from datetime import datetime
from os.path import join, isdir
from os import getcwd, makedirs
from subprocess import check_output


class CLI:
    def __init__(self,
                 code_maat_jar_file='code-maat.jar',
                 git_command='git',
                 java_command='java',
                 log_dir=join(getcwd(), '.logs')):
        self.log_dir = log_dir
        self.git_command = git_command
        self.java_command = java_command
        self.code_maat_jar_file = code_maat_jar_file

        if not isdir(log_dir):
            makedirs(self.log_dir)

    def generate_log(self, start_date=datetime.now(), end_date=datetime.now()):
        start_format = datetime.strftime(start_date, "%Y-%m-%d")
        end_format = datetime.strftime(end_date, "%Y-%m-%d")
        log_file_name = "log--%s--%s.log" % (start_format, end_format)
        log_file = join(self.log_dir, log_file_name)

        log_output = self._execute_git(
            "log",
            "--pretty=format:'[%h] %aN %ad %s'",
            "--date=short",
            "--numstat",
            ("--after=%s" % start_format),
            ("--before=%s" % end_format))

        with open(log_file, 'wb') as f:
            f.write(log_output)

        return log_file

    def _execute_git(self, command, *cli_args):
        return check_output([
            self.git_command,
            command,
            *cli_args])

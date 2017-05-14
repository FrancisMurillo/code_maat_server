from datetime import datetime
from os.path import join
from tempfile import gettempdir
from subprocess import call, check_output


class CLI:
    def __init__(self,
                 code_maat_jar_file='code-maat.jar',
                 git_command='git',
                 java_command='java'):
        self.log_dir = gettempdir()
        self.git_command = git_command
        self.java_command = java_command
        self.code_maat_jar_file = code_maat_jar_file

    def generate_log(self, start_date=datetime.now(), end_date=datetime.now()):
        start_format = datetime.strftime(start_date, "%Y-%m-%d")
        end_format = datetime.strftime(end_date, "%Y-%m-%d")
        log_file_name = "log--%s--%s.log" % (start_format, end_format)
        log_file = join(self.log_dir, log_file_name)

        log_output = check_output([
            self.git_command,
            "log",
            "--pretty=format:'[%h] %aN %ad %s'",
            "--date=short",
            "--numstat",
            ("--after=%s" % start_format),
            ("--before=%s" % end_format), ])

        with open(log_file, 'wb') as f:
            f.write(log_output)

        return log_file

from datetime import datetime
from os.path import join, isdir, splitext
from os import getcwd, makedirs, chdir
from subprocess import check_output


class CLI:
    def __init__(self,
                 code_maat_jar_file=join(getcwd(),  'code-maat.jar'),
                 git_command='git',
                 java_command='java',
                 log_dir=join(getcwd(), '.logs'),
                 git_dir=getcwd(),
                 **_keywords):
        self.git_dir = git_dir
        self.log_dir = log_dir
        self.git_command = git_command
        self.java_command = java_command
        self.code_maat_jar_file = code_maat_jar_file

        if not isdir(log_dir):
            makedirs(self.log_dir)

    def generate_log_file(self,
                          start_date=datetime.now(),
                          end_date=datetime.now()):
        start_format = datetime.strftime(start_date, "%Y-%m-%d")
        end_format = datetime.strftime(end_date, "%Y-%m-%d")
        log_file_name = "log--%s--%s.log" % (start_format, end_format)
        log_file = join(self.log_dir, log_file_name)

        log_output = self._execute_git(
            "log",
            "--pretty=format:[%h] %aN %ad %s",
            "--date=short",
            "--numstat",
            ("--after=%s" % start_format),
            ("--before=%s" % end_format))

        with open(log_file, 'wb') as f:
            f.write(log_output)

        return log_file

    def generate_summary_file(self, log_file):
        command_file = self._rename_extension(log_file, "--summary.csv")

        command_output = self._execute_code_maat(
            log_file,
            "summary")

        with open(command_file, 'wb') as f:
            f.write(command_output)

        return command_file

    def generate_coupling_file(self, log_file):
        command_file = self._rename_extension(log_file, "--coupling.csv")

        command_output = self._execute_code_maat(
            log_file,
            "coupling")

        with open(command_file, 'wb') as f:
            f.write(command_output)

        return command_file

    def generate_age_file(self, log_file):
        command_file = self._rename_extension(log_file, "--age.csv")

        command_output = self._execute_code_maat(
            log_file,
            "age")

        with open(command_file, 'wb') as f:
            f.write(command_output)

        return command_file

    def generate_absolute_churn_file(self, log_file):
        command_file = self._rename_extension(log_file, "--absolute-churn.csv")

        command_output = self._execute_code_maat(
            log_file,
            "abs-churn")

        with open(command_file, 'wb') as f:
            f.write(command_output)

        return command_file

    def generate_author_churn_file(self, log_file):
        command_file = self._rename_extension(log_file, "--author-churn.csv")

        command_output = self._execute_code_maat(
            log_file,
            "author-churn")

        with open(command_file, 'wb') as f:
            f.write(command_output)

        return command_file

    def generate_entity_churn_file(self, log_file):
        command_file = self._rename_extension(log_file, "--entity-churn.csv")

        command_output = self._execute_code_maat(
            log_file,
            "entity-churn")

        with open(command_file, 'wb') as f:
            f.write(command_output)

        return command_file

    def generate_entity_ownership_file(self, log_file):
        command_file = self._rename_extension(
            log_file, "--entity-ownership.csv")

        command_output = self._execute_code_maat(
            log_file,
            "entity-ownership")

        with open(command_file, 'wb') as f:
            f.write(command_output)

        return command_file

    def generate_entity_effort_file(self, log_file):
        command_file = self._rename_extension(
            log_file, "--entity-effort.csv")

        command_output = self._execute_code_maat(
            log_file,
            "entity-effort")

        with open(command_file, 'wb') as f:
            f.write(command_output)

        return command_file

    def _rename_extension(self, raw_file, new_extension):
        return splitext(raw_file)[0] + new_extension

    def _execute_git(self, command, *cli_args):
        temp_dir = getcwd()
        chdir(self.git_dir)

        output = check_output([
            self.git_command,
            command,
            *cli_args]).strip()

        chdir(temp_dir)

        return output

    def _execute_code_maat(self, log_file, command, *extra_args):
        temp_dir = getcwd()
        chdir(self.git_dir)

        output = check_output([
            self.java_command,
            "-jar",
            self.code_maat_jar_file,
            "-l",
            log_file,
            "-c",
            "git",
            "-a",
            command,
            *extra_args]).strip()

        chdir(temp_dir)

        return output

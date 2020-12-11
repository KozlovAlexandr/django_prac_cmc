import os
import subprocess
import tempfile
import json

from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded


@shared_task(soft_time_limit=10)
def compile_and_run(text, prog_input):
    try:
        with tempfile.NamedTemporaryFile(mode='w+t', delete=False, suffix='.out') as exec_file:

            result = {}

            try:

                args = ['g++', '-std=c++17', '-o', exec_file.name, '-x', 'c++', '-']
                compiler_process = subprocess.run(args=args, encoding='utf_8', stdout=subprocess.PIPE,
                                                  stderr=subprocess.STDOUT, input=text, check=True)

                if compiler_process.stdout:
                    result.update({'compiler_output': compiler_process.stdout})

                exec_file.close()
                args = ['firejail', '--shell=none', '--quiet', '--private', '--private-bin=/',  '--rlimit-nproc=100',  exec_file.name]
                process = subprocess.run(args=args, encoding='utf_8', stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE, input=prog_input)

                if process.stdout:
                    result.update({'stdout': process.stdout[:1000]})

                    if len(process.stdout) > 1000:
                        result.update({'stdout_cut': "true"})

                if process.stderr:
                    result.update({'stderr': process.stderr[:1000]})

                    if len(process.stderr) > 1000:
                        result.update({'stderr_cut': "true"})

                result.update({'return_code': process.returncode})

                return result

            except subprocess.CalledProcessError as error:

                return {'compiler_error': error.stdout}

            finally:

                try:
                    os.unlink(exec_file.name)
                except:
                    pass

    except SoftTimeLimitExceeded:

        return {'error': 'Timeout'}

    except:
        raise
        return {'error': 'Internal error'}
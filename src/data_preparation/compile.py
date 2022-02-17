import os
import subprocess
from typing import List
from joblib import Parallel, delayed
from tqdm import tqdm

from src.lib.submissions import Submission


def start_docker():
    command_start = "docker start cpp_compiler"
    res = subprocess.check_call(command_start, shell=True)
    assert res == 0


def stop_docker():
    command_start = "docker stop cpp_compiler"
    res = subprocess.check_call(command_start, shell=True)
    assert res == 0


def prepare_assemblers(submissions: List[Submission]):
    def f(s: Submission):
        if not os.path.isfile("assembler/{}.s".format(s.submission_id)):
            command = "docker exec cpp_compiler g++-9 -std=gnu++17 -w -O2 -DONLINE_JUDGE -I/opt/boost/gcc/include -L/opt/boost/gcc/lib -I/opt/ac-library -S /source_codes/{}.cpp".format(
                s.submission_id)
            res = subprocess.check_call(command, shell=True)
            assert res == 0
            res = subprocess.check_call("docker cp cpp_compiler:/{}.s ./assembler".format(s.submission_id), shell=True)
            assert res == 0
            res = subprocess.check_call("docker exec cpp_compiler rm {}.s".format(s.submission_id), shell=True)
            assert res == 0

    Parallel(n_jobs=-1)(delayed(f)(s) for s in tqdm(submissions))


def prepare_pps(submissions: List[Submission]):
    def f(s: Submission):
        if not os.path.isfile("pp/{}.cpp".format(s.submission_id)):
            command = "docker exec cpp_compiler g++-9 -std=gnu++17 -w -O2 -DONLINE_JUDGE -I/opt/boost/gcc/include -L/opt/boost/gcc/lib -I/opt/ac-library -E -P /source_codes/{}.cpp > pp/{}.cpp".format(
                s.submission_id, s.submission_id)
            res = subprocess.check_call(command, shell=True)
            assert res == 0

    Parallel(n_jobs=-1)(delayed(f)(s) for s in tqdm(submissions))


sub = load_all_available_submissions()
prepare_assemblers(sub)

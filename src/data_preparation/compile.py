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
        command = "docker exec cpp_compiler /bin/bash -c 'mkdir {} && cp /source_codes/{}.cpp /{}/Main.cpp'".format(
            s.submission_id, s.submission_id, s.submission_id
        )
        res = subprocess.check_call(command, shell=True)
        assert res == 0
        command = "docker exec cpp_compiler /bin/bash -c 'cd {} && g++-9 -std=gnu++17 -w -O2 -DONLINE_JUDGE -I/opt/boost/gcc/include -L/opt/boost/gcc/lib -I/opt/ac-library -S ./Main.cpp'".format(
            s.submission_id, s.submission_id
        )
        res = subprocess.check_call(command, shell=True)
        assert res == 0
        res = subprocess.check_call(
            "docker cp cpp_compiler:/{}/Main.s ./assembler/{}.s".format(
                s.submission_id, s.submission_id
            ),
            shell=True,
        )
        assert res == 0
        res = subprocess.check_call(
            "docker exec cpp_compiler rm -r {}".format(s.submission_id), shell=True
        )
        assert res == 0

    submissions = list(
        filter(
            lambda submission: not os.path.isfile(
                "assembler/{}.s".format(submission.submission_id)
            ),
            submissions,
        )
    )
    Parallel(n_jobs=-1)(delayed(f)(s) for s in tqdm(submissions))

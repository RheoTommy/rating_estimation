import os
import subprocess
from typing import List
from joblib import Parallel, delayed
from tqdm import tqdm

from src.lib.submissions import Submission, load_all_available_submissions


def prepare_assemblers(submissions: List[Submission]):
    def f(s: Submission):
        if not os.path.isfile("assembler/{}.s".format(s.submission_id)):
            command = "docker exec atc g++ -std=gnu++17 -w -O2 -DONLINE_JUDGE -I/opt/boost/gcc/include -L/opt/boost/gcc/lib -I/opt/ac-library -S /source_codes/{}.cpp".format(
                s.submission_id)
            res = subprocess.check_call(command, shell=True)
            assert res == 0
            res = subprocess.check_call("docker cp atc:/{}.s ./assembler".format(s.submission_id), shell=True)
            assert res == 0
            res = subprocess.check_call("docker exec atc rm {}.s".format(s.submission_id), shell=True)
            assert res == 0

    Parallel(n_jobs=-1)(delayed(f)(s) for s in tqdm(submissions))


def prepare_pps(submissions: List[Submission]):
    def f(s: Submission):
        if not os.path.isfile("pp/{}.cpp".format(s.submission_id)):
            command = "docker exec atc g++ -std=gnu++17 -w -O2 -DONLINE_JUDGE -I/opt/boost/gcc/include -L/opt/boost/gcc/lib -I/opt/ac-library -E -P /source_codes/{}.cpp > pp/{}.cpp".format(
                s.submission_id, s.submission_id)
            res = subprocess.check_call(command, shell=True)
            assert res == 0

    Parallel(n_jobs=-1)(delayed(f)(s) for s in tqdm(submissions))


sub = load_all_available_submissions()
prepare_assemblers(sub)
prepare_pps(sub)

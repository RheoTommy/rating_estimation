import asyncio
import websockets
import subprocess
import time

import numpy as np
import pandas as pd

from src.bin.random_forest import load_model
from src.data_preparation.compile import start_docker, stop_docker
from src.single_characteristics.analyze_characteristics import characteristics


def compile_once(code: str) -> str:
    tmp_id = int(time.time() * 10000000)

    try:
        with open("tmp/{}.cpp".format(tmp_id), "w") as f:
            f.write(code)

        command = "docker exec cpp_compiler /bin/bash -c 'mkdir {}'".format(tmp_id)
        res = subprocess.check_call(command, shell=True)
        if res != 0:
            print(1)
            return "error"

        command = "docker cp tmp/{}.cpp cpp_compiler:/{}/Main.cpp".format(tmp_id, tmp_id)
        res = subprocess.check_call(command, shell=True)
        if res != 0:
            print(2)
            return "error"

        command = "docker exec cpp_compiler /bin/bash -c 'cd {} && g++-9 -std=gnu++17 -w -O2 -DONLINE_JUDGE -I/opt/boost/gcc/include -L/opt/boost/gcc/lib -I/opt/ac-library -S ./Main.cpp'".format(
            tmp_id
        )
        res = subprocess.check_call(command, shell=True)
        if res != 0:
            print(3)
            return "error"

        res = subprocess.check_call(
            "docker cp cpp_compiler:/{}/Main.s ./tmp/{}.s".format(
                tmp_id, tmp_id
            ),
            shell=True,
        )
        if res != 0:
            print(4)
            return "error"

        res = subprocess.check_call(
            "docker exec cpp_compiler /bin/bash -c 'rm -r {}'".format(tmp_id), shell=True
        )
        if res != 0:
            print(5)
            return "error"

        with open("tmp/{}.s".format(tmp_id)) as f:
            pp = f.read()

        res = subprocess.check_call("rm tmp/*", shell=True)
        if res != 0:
            print(6)
            return "error"
    except Exception as e:
        print(e)
        return "error"

    return pp


def predict(code: str) -> float:
    pp = compile_once(code)
    if pp == "error":
        print("error")
        return np.nan
    sc = (code, pp)

    try:
        x = pd.DataFrame()
        for (func, func_name, subject) in characteristics:
            features = func([sc[subject]])
            x[func_name] = features

        x = x.values

        y = model.predict(x)

        return y[0]
    except Exception as e:
        print(e)
        return np.nan


async def echo(websocket, _path):
    async for message in websocket:
        await  websocket.send(str(predict(message)))


async def main():
    async with websockets.serve(echo, "127.0.0.1", 12345):
        await asyncio.Future()


model = load_model()
start_docker()
print("initialized docker")

asyncio.run(main())
print("initialized server")

stop_docker()

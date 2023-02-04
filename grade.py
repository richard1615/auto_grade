import os

# get submission input file

# create container from image
def run_container(id, extension, dir, timelimit):
    pwd = os.getcwd()
    os.system(f'docker run -v {pwd}/autoGrade/{dir}:/home/execution_user/{dir} bwh:latest {id} {extension} {dir} {timelimit} > result.txt')

def return_result():
    res_file = open('result.txt')
    res = res_file.read()

    if res.startswith("wrong output"):
        return "WA"
    elif res.startswith("time limit"):
        return "TLE"
    elif res.startswith("success"):
        return "AC"

# run container, get status
run_container("p1", "cpp", "p1", 1)
res = return_result()
print(res)
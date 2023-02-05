import os
from eval import grade
def evaluate(request):
    # submission = Submission.objects.get(pk=submission_id)
    # assignment = Assignment.objects.get(pk=assignment_id)
    file = 'p1-main.cpp'
    filename = file[file.rfind('/'):]
    id = filename[0:filename.find('-')]
    extension = filename[filename.rfind('.')+1:]
    dir = id
    timelimit = 1

    os.chdir('assignment_submissions/eval')
    os.system(f'mkdir {id} {id}/{id}-input {id}/{id}-output')
    os.system(f'cp ../../test_cases/{id}-input*.* {id}/{id}-input/')
    os.system(f'cp ../../test_cases/{id}-output*.* {id}/{id}-output/')
    os.system(f'cp ../../code/{id}-main.{extension} {id}/')

    grade.run_container(id, extension, dir, timelimit)
    res = grade.return_result()

    os.system(f'sudo rm -rf {id}')
    # os.system(f'rm -rf {id}')
    marks = {'AC': 100, 'WA': 0, 'TLE': 50}
    print(marks[res])
    # assignment.score = marks.get(res, -5)
    # assignment.save()
    #return redirect('assignments')
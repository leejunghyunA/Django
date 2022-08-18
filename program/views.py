from django.shortcuts import render

#inputdata 탬플릿을 랜더링 (입력)
def inputdata(request):
    return render(request, 'program/inputdata.html')

#result 탬플릿을 랜더링 (출력)
def result(request):

    # eval 함수 사용(숫자+문자를 계산해주는 함수)
    cal = request.GET['input_val']
    answer = eval(cal)
    return render(request, 'program/result.html', {'answer': answer})


    # # 두 수를 입력받아 더해서 출력 (a, b => GET방식 활용)
    # lis = []
    # lis.append(request.GET['input_val1'])
    # lis.append(request.GET['input_val2'])
    
    # sum = 0
    # for l in lis:
    #     sum += int(l)

    # answer = sum
    # return render(request, 'program/result.html', {'answer': answer, 'lis':lis})
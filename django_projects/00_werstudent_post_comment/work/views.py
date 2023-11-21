from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def work_handle(request):
    if request.method == "GET":
        return render(request, "work/work.html")
    elif request.method == "POST":
        # get value from POST

        number = request.POST.get("number")
        print(number)
        operation = request.POST.get("operation")
        print(operation)
        result_list = []
        result_sum = 0

        #change to list

        result_list = strToList(number)
        if len(result_list) == 0:
            return HttpResponse("wrong parameter")
        # judge and calculate
        if operation == "sum":
            result_sum = calSum(result_list)
            return render(request, "work/work.html", locals())
        elif operation == "fibo":
            if len(result_list) > 1:
                return HttpResponse("wrong parameter")
            else:
                sequence = fibonacci(result_list[0])
                return render(request, "work/work.html", locals())



def strToList(str):
    if str:
        list = [int(i) for i in str.split(",")]
        print(list)
        return list
    else:
        return []

def calSum(list):
    summe = 0
    for zahl in list:
        summe += zahl
    return summe

def fibonacci(n):
    sequence = [0, 1]
    if n <= 2:
        return sequence[:n]
    else:
        for i in range(2, n):
            next_number = sequence[i-1] + sequence[i-2]
            sequence.append(next_number)
        return sequence


def picker_handle(request):
    if request.method == "GET" :
        if not request.session.get("chosen_date"):
            request.session["chosen_data"] = ""
            return render(request, "work/picker.html")
        else:
            return render(request, "work/picker.html", {"chosen_date":  request.session.get("chosen_date", "1970-01-01")})
    elif request.method == "POST":
        chosen_date = request.POST.get("chosen_date")
        request.session["chosen_data"] = chosen_date
        return render(request, "work/picker.html", {'chosen_date': chosen_date})


def picker_handle(request):
    # first save data in session
    if request.method == 'POST':
        chosen_date = request.POST.get('chosen_date')
        print(chosen_date)
        request.session['chosen_date'] = chosen_date
    else:
        chosen_date = request.session.get('chosen_date', '')

    return render(request, 'work/picker.html', {'chosen_date': chosen_date})

def picker_handle2(request):
    if request.method == "POST" :
        if not request.POST.get("chosen_date2"):
            return render(request, "work/picker.html")
        else:
            print("else")
            chosen_date2 = request.POST.get("chosen_date2")
            return render(request, "work/picker.html", {"chosen_date2":  chosen_date2})
    else:
        chosen_date2 = request.POST.get("chosen_date2")
        return render(request, "work/picker.html", {'chosen_date2': chosen_date2})

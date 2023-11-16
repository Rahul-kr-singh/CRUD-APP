from django.shortcuts import render, redirect
from .models import Employee
from .forms import EmployeeForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def employees_list(request):
    # employees = Employee.objects.all()
    # page = request.GET.get('page', 1)

    # paginator = Paginator(employees, 10)
    # try:
    #     users = paginator.page(page)
    # except PageNotAnInteger:
    #     users = paginator.page(1)
    # except EmptyPage:
    #     users = paginator.page(paginator.num_pages)
    # print(employees)

    search_query = ""

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    employees = Employee.objects.filter(
        Q(emp_name__icontains=search_query) | 
        Q(emp_role__icontains=search_query) |
        Q(emp_salary__icontains=search_query)
    )

    context = {
        'employees': employees,
        'search_query': search_query,
        # 'users': users,
    }
    return render(request, 'emp/list.html',context)


def create_employee(request):
    form = EmployeeForm()

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employees-list')

    context = {
        'form': form,
    }
    return render(request, 'emp/create.html', context)


def edit_employee(request, pk):
    employee = Employee.objects.get(id=pk)
    form = EmployeeForm(instance=employee)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees-list')

    context = {
        'employee': employee,
        'form': form,
    }
    return render(request, 'emp/edit.html', context)


def delete_employee(request, pk):
    employee = Employee.objects.get(id=pk)

    if request.method == 'POST':
        employee.delete()
        return redirect('employees-list')

    context = {
        'employee': employee,
    }
    return render(request, 'emp/delete.html', context)
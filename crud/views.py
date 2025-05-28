from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders, Users
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('user_list')
    else:
        form = UserRegistrationForm()

        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')


        context = {'form': form}
        return render(request, 'user/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('user_list')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('user_list')
            else:
                messages.error(request, "Username or password is incorrect")

        return render(request, 'user/login.html')



def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def genders_list(request):
    try:
        genders = Genders.objects.all()

        data = {
            'genders':genders 
        }
        return render(request, 'gender/GendersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during load genders: {e}')

@login_required(login_url='login')
def add_gender(request):
    try:
        if request.method == 'POST':
            gender = request.POST.get('gender')

            Genders.objects.create(gender=gender).save()
            messages.success(request, 'Gender added successfully!')
            return redirect('/gender/list')
        else:
            return render(request, 'gender/AddGender.html')
    
    except Exception as e:
        return HttpResponse(f'Error occured during add gender: {e}')

@login_required(login_url='login')
def edit_gender(request, genderId):
    try:
        if request.method == 'POST':
            genderObj = Genders.objects.get(pk=genderId)

            gender = request.POST.get('gender')
            
            genderObj.gender = gender
            genderObj.save()

            messages.success(request, 'Gender updated successfully!')

            data = {
                'gender': genderObj
            }

            return render(request, 'gender/EditGender.html', data)

        else:    
            genderObj = Genders.objects.get(pk=genderId)
            
            data = {
                'gender': genderObj
            }

            return render(request, 'gender/EditGender.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during edit gender: {e}')

@login_required(login_url='login')
def delete_gender(request, genderId):
    try:
        if request.method == 'POST':
            genderObj = Genders.objects.get(pk=genderId)
            genderObj.delete()

            messages.success(request, 'Gender deleted successfully!')
            return redirect('/gender/list/')

        else:
            genderObj = Genders.objects.get(pk=genderId)
                
            data = {
                'gender': genderObj
            }

            return render(request, 'gender/DeleteGender.html', data)

    except Exception as e:
        return HttpResponse(f'Error occured during delete gender: {e}')

@login_required(login_url='login')
def user_list(request):
    try:
        userObj = Users.objects.select_related('gender')

        data = {
            'users': userObj
        }
    
        return render(request, 'user/UsersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during load users: {e}')

@login_required(login_url='login')
def add_user(request):
    try:
        if request.method == 'POST':
            fullName = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birthDate = request.POST.get('birth_date')
            address = request.POST.get('address')
            contactNumber = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirmPassword = request.POST.get('confirm_password')

            if password != confirmPassword:
                messages.error(request, "Passwords do not match.")
                return redirect('add_user')

            Users.objects.create(
                full_name=fullName,
                gender=Genders.objects.get(pk=gender),
                birth_date=birthDate,
                address=address,
                contact_number=contactNumber,
                email=email,
                username=username,
                password=make_password(password)
            ).save()

            messages.success(request, 'User added successfully!')
            return redirect('/user/add/')

        else:
            genderObj = Genders.objects.all()

            data = {
                'genders': genderObj
            }

            return render(request, 'user/AddUser.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during add user: {e}')

@login_required(login_url='login')
def edit_user(request, userId):
    try:
        userObj = Users.objects.get(pk=userId)
        genderObj = Genders.objects.all()

        if request.method == 'POST':
            userObj.full_name = request.POST.get('full_name')
            gender_id = request.POST.get('gender')

            try:
                userObj.gender = Genders.objects.get(pk=gender_id)
            except Genders.DoesNotExist:
                messages.error(request, "Selected gender does not exist.")
                return render(request, 'user/EditUser.html', {'user': userObj, 'genders': genderObj})

            userObj.birth_date = request.POST.get('birth_date')
            userObj.address = request.POST.get('address')
            userObj.contact_number = request.POST.get('contact_number')
            userObj.email = request.POST.get('email')
            userObj.username = request.POST.get('username')

            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password or confirm_password:
                if password == confirm_password:
                    userObj.password = make_password(password)
                else:
                    messages.error(request, "Passwords do not match.")
                    return render(request, 'user/EditUser.html', {'user': userObj, 'genders': genderObj})

            userObj.save()
            messages.success(request, 'User updated successfully!')
            return redirect('/user/list/')

        return render(request, 'user/EditUser.html', {
            'user': userObj,
            'genders': genderObj
        })

    except Exception as e:
        return HttpResponse(f'Error occurred during edit user: {e}')

@login_required(login_url='login')
def delete_user(request, userId):
    try:
        userObj = Users.objects.get(pk=userId)

        if request.method == 'POST':
            userObj.delete()
            messages.success(request, 'User deleted successfully!')
            return redirect('/user/list/')

        else:
            data = {
                'user': userObj
            }
            return render(request, 'user/DeleteUser.html', data)

    except Exception as e:
        return HttpResponse(f'Error occurred during delete user: {e}')

@login_required(login_url='login')
def sidebar_view(request):
    return render(request, 'user/sidebar.html')

该文档只是对django的最基本流程进行一下总结
[django tutorial](https://docs.djangoproject.com/en/2.2/intro/tutorial01/)


## 建project 和 App

The difference between a project and an app. An app is a Web application that does something – e.g., a Weblog system, a database of public records or a simple poll app. A project is a collection of configuration and apps for a particular website. A project can contain multiple apps. An app can be in multiple projects.
```
#Create the project
django-admin startproject mysite

#The following folders will be created

mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        wsgi.py

# Run the server:
python manage.py runserver 0:8000
# 0 is a shortcut for 0.0.0.0, the server will listen on port 8000
```


```
#Create the app
$ python manage.py startapp polls
#That’ll create a directory polls, which is laid out like this:
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```

## View And Url
In the view file polls/views.py
```
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

#can be also more complex with a page


def index(request):
    
    #read the airline list from Airlines table 
    select_list = Airlines.objects.values('airline').distinct()
    airline_list = [select["airline"] for select in select_list]

    #put airline in the context for the page rendering
    context = {'airline_list': list(set(airline_list))}

    return render(request, 'ibean/index.html', context)
```
To call the view, we need to map it to a URL - and for this we need a URLconf, create a file called urls.py. Your app directory should now look like:

```
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    urls.py
    views.py
```


In the polls/urls.py file include the following code:

```
polls/urls.py¶
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

The next step is to point the root URLconf at the polls.urls module. In mysite/urls.py, add an import for django.urls.include and insert an include() in the urlpatterns list, so you have:

```
mysite/urls.py¶
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

## 使用一个已经存在的数据库
首先是在project下的settings.py中定义数据库相关信息，host, poer, user, etc. Django comes with a utility called inspectdb that can create models by introspecting an existing database. You can view the output by running this command:
```
#Ibean is the table name
python manage.py inspectdb ibean > ibean.txt
```
copy the output to the models.py

"""NFQA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from QAS.views import chat, corpus, home, login, upload, notice, user, docs


urlpatterns = [
    path('', home.HomeView.as_view()),
    path('api/', home.APIHomeView.as_view()),

    path('api/sysinfo/', home.SystemView.as_view()),

    path('api/login/', login.LoginAPIView.as_view()),

    path('api/user/', user.UserListView.as_view()),
    path('api/user/<int:pk>/', user.UserView.as_view()),

    path('api/word/', notice.NoticeListView.as_view()),
    path('api/word/<int:pk>', notice.NoticeView.as_view(), name='notice-detail'),

    path('api/neo4j/', chat.Neo4jView.as_view()),
    path('api/neo4j/<int:pk>', chat.Neo4jView.as_view()),

    path('api/upload/', upload.UploadFileListView.as_view()),
    path('api/upload/<int:pk>/', upload.UploadFileView.as_view()),

    path('api/corpus/', corpus.CorpusListView.as_view()),

    path('api/docs/', docs.SwaggerSchemaView.as_view()),

]

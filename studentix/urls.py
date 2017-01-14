

from django.conf.urls import url

from . import views 

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^userLogin$', views.userLogin, name='userLogin'),
    url(r'^logout$',views.logoutme,name='logout'),
    url(r'^auth_view$',views.auth_view,name='auth_view'),
    url(r'^studentSignup$', views.studentSignup, name='studentSignup'),
    url(r'^home$',views.userHome,name='userHome'),
    url(r'^home/sendEmail$',views.sendEmail,name='sendEmail'),
    url(r'^parentLogin$',views.parentLogin,name='parentLogin'),
    url(r'^parentHome/(?P<username>\w+)$',views.parentHome,name='parentHome'),
    url(r'^allCourse/$',views.allCourse,name='allCourse'),
    url(r'^courseDetail/(?P<coursename>\w+)$',views.courseDetail,name='courseDetail'),
    url(r'^enrol/(?P<coursename>\w+)$',views.enrol,name='enrol'),
    url(r'^(?P<coursename>\w+)/(?P<pk>[0-9]+)$',views.content,name='content'),
    url(r'^(?P<coursename>\w+)/mid_term_quiz$',views.mid_term_quiz,name='mid_term_quiz'),
    url(r'^(?P<coursename>\w+)/end_term_quiz$',views.end_term_quiz,name='end_term_quiz'),
    url(r'^(?P<coursename>\w+)/mid_term_evaluation$',views.mid_term_evaluation,name='mid_term_evaluation'),
    url(r'^(?P<coursename>\w+)/end_term_evaluation$',views.end_term_evaluation,name='end_term_evaluation'),
    url(r'^(?P<coursename>\w+)/addContent$',views.addContent,name='addContent'),
    url(r'^(?P<coursename>\w+)/addNotice$',views.addNotice,name='addNotice'),
    url(r'^(?P<coursename>\w+)/add_mid_term_quiz$',views.add_mid_term_quiz,name='add_mid_term_quiz'),
    url(r'^(?P<coursename>\w+)/add_end_term_quiz$',views.add_end_term_quiz,name='add_end_term_quiz'),
    url(r'^content_succefully_added$',views.content_succefully_added,name='content_succefully_added'),
    url(r'^notice_succefully_added$',views.notice_succefully_added,name='notice_succefully_added'),
    url(r'^mid_term_quiz_succefully_added$',views.mid_term_quiz_succefully_added,name='mid_term_quiz_succefully_added'),
    url(r'^end_term_quiz_succefully_added$',views.end_term_quiz_succefully_added,name='end_term_quiz_succefully_added'),
    url(r'^email_succefully_added$',views.email_succefully_added,name='email_succefully_added'),
    # url()
    #url(r'^(?P<course>\w+)/home$'views.userHome,name='userHome'),

]
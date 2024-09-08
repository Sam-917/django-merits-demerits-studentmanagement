from django import forms
from .models import MeritStudent, DemeritStudent, Grade, Class
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm 
 

class MeritStudentForm(forms.ModelForm):
    class Meta:
        model = MeritStudent
        fields = ('student_name', 'teacher_responsible', 'ic_number', 'achievement', 'grade', 'class_name')
       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grade'].queryset = Grade.objects.all()

        if 'grade' in self.data:
            try:
                grade_id = int(self.data.get('grade'))
                self.fields['class_name'].queryset = Class.objects.filter(grade_id=grade_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['class_name'].queryset = Class.objects.none()
        elif self.instance.pk and self.instance.grade:
            self.fields['class_name'].queryset = Class.objects.filter(grade=self.instance.grade).order_by('name')
        else:
            self.fields['class_name'].queryset = Class.objects.none()

class DemeritStudentForm(forms.ModelForm):
    class Meta:
        model = DemeritStudent
        fields = ('student_name', 'teacher_responsible', 'ic_number', 'issue', 'grade', 'class_name')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['grade'].queryset = Grade.objects.all()
            self.fields['class_name'].queryset = Class.objects.all()
    
class SignUpForm(UserCreationForm): 
    class Meta: 
        model = User 
        fields = ('username', 'email', 'password1', 'password2') 


from rest_framework import serializers
from ..models import Subject, Course


class SubjectSerializer(serializers.ModelSerializer):
    class Meta: # specify the model to serialize and the fields to be included for serialization
        model = Subject
        fields = ['id', 'title', 'slug']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview', 'created', 'owner', 'modules']
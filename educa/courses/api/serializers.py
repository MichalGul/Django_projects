from rest_framework import serializers
from ..models import Subject, Course, Module


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta: # specify the model to serialize and the fields to be included for serialization
        model = Subject
        fields = ['id', 'title', 'slug']


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview', 'created', 'owner', 'modules']




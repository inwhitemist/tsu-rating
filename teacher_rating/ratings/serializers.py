from rest_framework import serializers
from .models import Teacher, Action, Review

class TeacherSerializer(serializers.ModelSerializer):
    rank = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = '__all__'

    def get_rank(self, obj):
        return obj.get_rank()

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

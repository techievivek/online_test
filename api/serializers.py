from rest_framework import serializers
from yaksh.models import Course,LearningModule,LearningUnit,Lesson,Quiz
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model=Quiz
        fields=['description','pass_criteria','attempts_allowed']
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lesson
        fields=['name','description','html_data','video_file']
class LearningUnitSerializer(serializers.ModelSerializer):
    lesson=LessonSerializer()
    quiz=QuizSerializer()
    class Meta:
        model=LearningUnit
        fields=['lesson','quiz']
class LearningModuleSerializer(serializers.ModelSerializer):
    learning_unit=LearningUnitSerializer(many=True)
    class Meta:
        model=LearningModule
        fields=['name','description','learning_unit']
class CourseSerializer(serializers.ModelSerializer):
    creator=serializers.StringRelatedField()
    # students=serializers.StringRelatedField(many=True)
    # requests=serializers.StringRelatedField(many=True)
    # rejected=serializers.StringRelatedField(many=True)
    # teachers=serializers.StringRelatedField(many=True)
    # learning_module=serializers.StringRelatedField(many=True)
    learning_module=LearningModuleSerializer(many=True)
    # grading_system=serializers.StringRelatedField()
    class Meta:
        model=Course
        fields=['name','enrollment','active','code','hidden','creator','created_on','is_trial','instructions','view_grade','learning_module',
        'start_enroll_time','end_enroll_time']
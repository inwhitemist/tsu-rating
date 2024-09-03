from django.shortcuts import render, redirect
from .models import Teacher, Action, Review  # Импортируем Review
from .forms import ActionForm
from rest_framework import viewsets
from .serializers import TeacherSerializer, ActionSerializer, ReviewSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

def add_action(request):
    if request.method == 'POST':
        form = ActionForm(request.POST)
        if form.is_valid():
            action = form.save(commit=False)
            action.status = 'pending'
            action.save()
            return redirect('action_success')
    else:
        form = ActionForm()

    return render(request, 'ratings/add_action.html', {'form': form})

def action_success(request):
    return render(request, 'ratings/action_success.html')

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

    def get_queryset(self):
        status = self.request.query_params.get('status')
        if status:
            return self.queryset.filter(status=status)
        return self.queryset

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        action = self.get_object()
        action.status = 'approved'
        action.save()
        # Обновляем рейтинг преподавателя после утверждения поступка
        teacher = action.teacher
        teacher.update_rating()
        return Response({'status': 'Action approved'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        action = self.get_object()
        action.status = 'rejected'
        action.save()
        # Обновляем рейтинг преподавателя после отклонения поступка
        teacher = action.teacher
        teacher.update_rating()
        return Response({'status': 'Action rejected'})

# Новый ViewSet для отзывов
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        teacher_id = self.request.query_params.get('teacher')
        if teacher_id:
            return self.queryset.filter(teacher_id=teacher_id)
        return self.queryset

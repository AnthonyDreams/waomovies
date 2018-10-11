from rest_framework import serializers

from apps.comentarios.models import Post


class ComentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ('id', 'user', 'content', 'timestamp', 'slug', 'respuestas', 'vote', 'unvote')

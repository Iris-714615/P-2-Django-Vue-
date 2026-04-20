from rest_framework import serializers
from . import models
class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.People
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    uploader = serializers.SerializerMethodField(read_only=True)
    def get_uploader(self, obj):
        return obj.people.name
    class Meta:
        model = models.Article
        fields = '__all__'

    def validate_title(self,value):
        if not value.startswith("JY"):
            raise serializers.ValidationError("标题要以JY开头")
        return value
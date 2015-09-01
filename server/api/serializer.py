from rest_framework import serializers
from api import models


__author__ = 'abdullah'


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Content


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Content
        fields = ('title', 'link', 'is_active', 'is_for_static_content')


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Device


class SoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Software


class StageMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StageMaterial


class CompositionSerializer(serializers.ModelSerializer):
    # owner = UserSerializer()
    softwares = SoftwareSerializer(many=True)
    devices = DeviceSerializer(many=True)
    stage_materials = StageMaterialSerializer(many=True)
    contest = serializers.PrimaryKeyRelatedField(queryset=models.Contest.objects.all())
    owner = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all())
    # owner = UserSerializer()
    # contest = ContestSerializer()

    softwares_data = None
    devices_data = None
    stage_materials_data = None
    composition = None

    def create(self, validated_data):

        softwares_data = validated_data.pop('softwares')
        devices_data = validated_data.pop('devices')
        stage_materials_data = validated_data.pop('stage_materials')

        composition = models.Composition.objects.create(**validated_data)

        composition = self.create_or_update_lists(composition, softwares_data, devices_data, stage_materials_data)

        # self.create_or_update_lists()

        composition.save()

        print 'composition is created'

        return composition

    def update(self, instance, validated_data):

        softwares_data = validated_data.pop('softwares')
        devices_data = validated_data.pop('devices')
        stage_materials_data = validated_data.pop('stage_materials')

        instance.name = validated_data['name']
        instance.url = validated_data['url']

        instance = self.create_or_update_lists(instance, softwares_data, devices_data, stage_materials_data)

        instance.save()

    def create_or_update_lists(self, composition, softwares_data, devices_data, stage_materials_data):
        softwares_list = []
        for software_data in softwares_data:
            (s, created) = models.Software.objects.get_or_create(**software_data)

            if s:
                softwares_list.append(s)

        devices_list = []
        for device_data in devices_data:
            (d, created) = models.Device.objects.get_or_create(**device_data)

            if d:
                devices_list.append(d)

        stage_materials_list = []
        for stage_material_data in stage_materials_data:
            (sm, created) = models.StageMaterial.objects.get_or_create(**stage_material_data)

            if sm:
                stage_materials_list.append(sm)

        composition.softwares = softwares_list
        composition.devices = devices_list
        composition.stage_materials = stage_materials_list

        return composition

    class Meta:
        model = models.Composition
        depth = 1
        # fields = ('softwares',)


class CompositionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Composition
        depth = 1


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vote


class TrackUploadSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = models.TrackUpload
        read_only_fields = ('created', 'datafile', 'owner')

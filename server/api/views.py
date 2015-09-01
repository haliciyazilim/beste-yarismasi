from datetime import datetime

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from api.models import Content, User, Composition, Device, Contest, Software, StageMaterial, Vote
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializer import ContentSerializer, UserSerializer, LinkSerializer, \
    DeviceSerializer, SoftwareSerializer, StageMaterialSerializer, CompositionSerializer, \
    ContestSerializer, VoteSerializer, CompositionListSerializer

__author__ = 'abdullah'


def get_client_ip(request):
    ip = request.META.get('HTTP_CF_CONNECTING_IP')
    if ip is None:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_current_contest():
    current_date = datetime.now()
    current_contest = Contest.objects.filter(start_date__lt=current_date, finish_date__gt=current_date)

    if len(current_contest) == 1:
        return current_contest[0]
    else:
        return None


class Contents(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, content_link=None, format=None):

        print 'Contents are Called'

        print request.user
        print request.auth
        print request.META.get('HTTP_AUTHORIZATION')

        if content_link:
            content = Content.objects.get(link=content_link)
            serializer = ContentSerializer(content)

            # print '%s: %s' % content_link, content
            return Response(serializer.data)
        else:
            contents = Content.objects.filter(category_name='index')
            print 'link contents: %s' % contents
            serializer = ContentSerializer(contents, many=True)

            return Response(serializer.data)


class Links(APIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (AllowAny,)

    def get(self, request):
        links = Content.objects.filter(category_name='link')
        serializer = LinkSerializer(links, many=True)

        return Response(serializer.data)


class Users(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class TrackRequirements(APIView):
    def get(self, request, format=None):
        current_contest = Contest.objects.latest('year')
        devices = Device.objects.all()
        softwares = Software.objects.all()
        stage_materials = StageMaterial.objects.all()

        contest_serializer = ContestSerializer(current_contest)
        devices_serializer = DeviceSerializer(devices, many=True)
        software_serializer = SoftwareSerializer(softwares, many=True)
        stage_material_serializer = StageMaterialSerializer(stage_materials, many=True)

        return Response({'current_contest': contest_serializer.data,
                         'devices': devices_serializer.data,
                         'softwares': software_serializer.data,
                         'stage_materials': stage_material_serializer.data})


class VoteView(APIView):
    def post(self, request, format=None):
        is_qualified = request.data.get('is_qualified', None)
        is_finalist = request.data.get('is_finalist', None)
        vote_value = request.data.get('value', None)
        composition_id = request.data.get('composition', None)

        if is_qualified is not None and is_finalist is not None and composition_id:
            composition = Composition.objects.get(id=composition_id)

            composition.is_qualified = is_qualified
            composition.is_finalist = is_finalist
            composition.save()

            serializer = CompositionSerializer(composition)
            return Response(data=serializer.data)

        elif vote_value is not None and composition_id:
            ip = get_client_ip(request)
            current_contest = get_current_contest()
            composition = Composition.objects.get(id=composition_id)

            vote, created = Vote.objects.update_or_create(ip=ip, composition_id=composition_id, defaults={
                'contest': current_contest,
                'value': vote_value
            })

            # vote = Vote.objects.filter(ip=ip, composition=composition)
            #
            # if len(vote) == 0:
            #     vote = Vote(ip=ip, composition=composition, contest=current_contest, value=vote_value)

            if created is False:
                print 'create edilmedi'
            else:
                print 'create edildi.'

            print vote

            serializer = VoteSerializer(vote)
            return Response(data=serializer.data)

        return Response(status.HTTP_304_NOT_MODIFIED)


class CompositionView(APIView):
    def get(self, request, user_id=None, list_type=None, format=None):

        compositions = None
        if user_id:
            compositions = Composition.objects.filter(owner=user_id)
        elif list_type:

            if list_type == 'finalist':
                current_contest = get_current_contest()
                compositions = Composition.objects.filter(contest=current_contest, is_finalist=True)

                ip = get_client_ip(request)

                votes = Vote.objects.filter(ip=ip)

                votes_serializer = VoteSerializer(votes, many=True)

                compositions_serializer = CompositionListSerializer(compositions, many=True)
                return Response(data={'compositions': compositions_serializer.data,
                                      'votes': votes_serializer.data}, status=status.HTTP_200_OK)
        else:
            current_contest = get_current_contest()
            compositions = Composition.objects.filter(contest=current_contest)

        serializer = CompositionListSerializer(compositions, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id=None, format=None):

        # try:
        request_token = request.auth
        user = request.user
        track = request.data

        # print 'user id: %s' % user.id
        track['owner'] = user.id

        print request_token
        print user
        print track

        req_composition_name = track['name']
        print req_composition_name

        req_composition_id = track['id']
        print req_composition_id

        req_softwares = track['softwares']
        print req_softwares

        req_url = track['url']
        print req_url

        serializer = CompositionSerializer(data=track)

        if serializer.is_valid():
            print 'composition is valid'

            if req_composition_id:
                print 'composition should updated'
                composition_instance = Composition.objects.get(pk=req_composition_id)
                serializer.update(composition_instance, serializer.data)
            else:
                serializer.save()
        else:
            print 'composition is no valid %s' % serializer.errors

        # composition.softwares = softwares

        return Response(status=status.HTTP_200_OK)

        # except Exception:

        # print Exception.args
        # return Response(status=status.HTTP_400_BAD_REQUEST)


class ContestView(APIView):

    def get(self, request, contest_year=None, format=None):

        if contest_year is None:
            current_contest = get_current_contest()
            contests = Contest.objects.exclude(pk=current_contest.id)
            serializer = ContestSerializer(contests, many=True)

            return Response(data=serializer.data)
        else:
            contest = Contest.objects.get(year=contest_year)
            compositions = Composition.objects.filter(contest_id=contest.id)

            contest_serializer = ContestSerializer(contest)
            compositions_serializer = CompositionListSerializer(compositions, many=True)

            return Response(data={'contest': contest_serializer.data, 'tracks': compositions_serializer.data})


#
# class TrackUploadView(APIView):
#     parser_classes = (FileUploadParser, MultiPartParser)
#
#     def post(self, request):
#
#         try:
#             print 'TrackUploadView'
#             print request.data
#
#             request_token = request.auth
#             username = request.data['username']
#
#             track = request.data['track']
#             print track['devices']
#             # devices = track['devices']
#
#             # print devices
#             # softwares = track['softwares']
#             # stage_materials = track['stage_materials']
#             #
#             # composition_name = track.name
#
#             composition_serializer = CompositionSerializer(data=track)
#
#             if composition_serializer.is_valid():
#                 print 'composition is valid'
#             else:
#                 print 'composition is not valid'
#                 print composition_serializer.error_messages
#                 return Response(composition_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#             # if not request_token:
#             #     return Response(status=status.HTTP_403_FORBIDDEN)
#
#             composition = None
#             data = None
#             track = request.FILES['file']
#
#             if not track:
#                 print 'track is not exist'
#             else:
#                 print 'track exist'
#
#             # name
#             # owner
#             # contest
#             # file
#             # devices
#             # softwares
#             # stageMaterials
#
#             # composition = Composition()
#             # composition.name = composition_name
#             # composition.owner = User.objects.get(username)
#             # composition.contest = Contest.objects.order_by('year').last()
#             # composition.file = track
#             # composition.save()
#             #
#             # for device_name in devices:
#             #     if not device_name or len(device_name) < 2:
#             #         continue
#             #     device = Device.objects.get_or_create(name=device_name)
#             #     composition.devices.add(device)
#             #
#             # for software_name in softwares:
#             #     if not software_name or len(software_name) < 2:
#             #         continue
#             #     software = Software.objects.get_or_create(name=software_name)
#             #     composition.softwares.add(software)
#             #
#             # for stage_material_name in stage_materials:
#             #     if not stage_material_name or len(stage_material_name) < 2:
#             #         continue
#             #     stage_material = Software.objects.get_or_create(name=stage_material_name)
#             #     composition.stage_materials.add(stage_material)
#
#             return Response(status=status.HTTP_200_OK)
#         except Exception:
#             return Response(composition_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class FileUploadViewSet(ModelViewSet):
#     queryset = TrackUpload.objects.all()
#     serializer_class = TrackUploadSerializer
#     parser_classes = (MultiPartParser, FormParser,)
#
#     def get_object(self):
#         print 'FileUploadViewSet get is ok'
#
#     def get_queryset(self, serializer):
#         serializer.save(owner=User.objects.all()[0],
#                         datafile=self.request.data.get('datafile'))
#
#     def perform_create(self, serializer):
#         print 'FileUploadViewSet perform_create is ok'
#         # serializer.save(owner=self.request.user,
#         #                 datafile=self.request.data.get('datafile'))

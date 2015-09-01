# -*- coding: utf-8 -*-
import csv
import datetime

__author__ = 'abdullah'

from api.models import Content, Device, Software, StageMaterial, Contest, Composition, User
from django.core.management import BaseCommand


class Command(BaseCommand):
    # Show this when the user types help
    help = "Create base contents and save to database"

    # A command must define handle()
    def handle(self, *args, **options):

        try:

            contest = Contest.objects.all()
            contest.delete()

            contest_2014 = Contest()
            contest_2014.year = 2014
            contest_2014.theme = 'Ritim'
            contest_2014.poster = 'http://beste.halici.com.tr/afis/2014.jpg'
            contest_2014.start_date = datetime.datetime(2014, 6, 1, 0, 0)
            contest_2014.final_date = datetime.datetime(2014, 11, 1, 0, 0)
            contest_2014.finish_date = datetime.datetime(2014, 12, 15, 0, 0)
            contest_2014.save()

            contest_2015 = Contest()
            contest_2015.year = 2015
            contest_2014.theme='Attila Özdemiroğlu'
            contest_2014.poster = 'http://beste.halici.com.tr/afis/2015.jpg'
            contest_2015.start_date = datetime.datetime(2015, 6, 1, 0, 0)
            contest_2015.final_date = datetime.datetime(2015, 11, 1, 0, 0)
            contest_2015.finish_date = datetime.datetime(2015, 12, 15, 0, 0)
            contest_2015.save()

            devices = Device.objects.all()
            devices.delete()

            device = Device()
            device.name = 'Bilgisayar'
            device.save()

            softwares = Software.objects.all()
            softwares.delete()

            software = Software()
            software.name = 'FL Studio'
            software.save()

            stage_materials = StageMaterial.objects.all()
            stage_materials.delete()

            stage_material = StageMaterial()
            stage_material.name = 'Gitar'
            stage_material.save()

            contents = Content.objects.all()
            contents.delete()

            content_file = open('default_contents/api_content.csv', 'rb')
            reader = csv.reader(content_file)

            for row in reader:
                content = Content()
                content.create_date = row[1]
                content.title = row[2]
                content.link = row[3]
                content.content = row[4]
                content.category_name = row[5]
                content.is_active = True if row[7] == '1' else False
                content.is_for_static_content = True if row[8] == '1' else False

                content.save()

            content_vote=Content()
            content_vote.title = 'Oylama'
            content_vote.link='oylama'
            content_vote.category_name = 'link'
            content_vote.is_active = True
            content_vote.is_for_static_content = False
            content_vote.save()

            users = User.objects.all()
            users.delete()

            user = User()
            user.username = 'karacabey'
            user.email = 'siyahsuskunluk@gmail.com'
            user.first_name = 'Abdullah'
            user.last_name = 'Karacabey'
            user.set_password('674311')
            user.addres = 'Bağlum'
            user.city = 'Ankara'
            user.save()

            compositions = Composition.objects.all()
            compositions.delete()

            composition_1 = Composition()
            composition_1.owner=user
            composition_1.contest=contest_2014
            composition_1.name = 'İlk Şarkı'
            composition_1.url = 'https://s3-eu-west-1.amazonaws.com/gong-ir/temp_attachments/beste/1441108257899wjzK3Htv'
            composition_1.save()
            composition_1.softwares = [software]
            composition_1.devices = [device]
            composition_1.stage_materials = [stage_material]


            composition_2 = Composition(owner=user, contest=contest_2014)
            composition_2.name = 'İkinci Şarkı'
            composition_2.url = 'https://s3-eu-west-1.amazonaws.com/gong-ir/temp_attachments/beste/1441108257899wjzK3Htv'
            composition_2.save()
            composition_2.softwares = [software]
            composition_2.devices = [device]
            composition_2.stage_materials = [stage_material]

            composition_3 = Composition(owner=user, contest=contest_2015)
            composition_3.name = 'Üçüncü Şarkı'
            composition_3.url = 'https://s3-eu-west-1.amazonaws.com/gong-ir/temp_attachments/beste/1441108257899wjzK3Htv'
            composition_3.save()
            composition_3.softwares = [software]
            composition_3.devices = [device]
            composition_3.stage_materials = [stage_material]

            composition_4 = Composition(owner=user, contest=contest_2015)
            composition_4.name = 'Dördüncü Şarkı'
            composition_4.url = 'https://s3-eu-west-1.amazonaws.com/gong-ir/temp_attachments/beste/1441108257899wjzK3Htv'
            composition_4.save()
            composition_4.softwares = [software]
            composition_4.devices = [device]
            composition_4.stage_materials = [stage_material]

            composition_1.save()
            composition_2.save()
            composition_3.save()
            composition_4.save()



            print 'Default contents are created'
        except IOError:
            print 'File is not found'

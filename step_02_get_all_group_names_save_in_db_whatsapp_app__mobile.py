import sys

import selenium
import sqlalchemy
from appium import webdriver as driver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
import time

from All_Dabase_Tables_Classes import Group_Txt_Export
from android_global_method import Myandroid
from All_Dabase_Tables_Classes import Group_name_table, connect_to_database
from mongodb_connection import MondoBDConnection
from myconfiguration import step_02_last_group_name, deviceName

wait_time = 0.8


class Whatsapp_automate():
    driver = None
    contact_name = []
    group_not_found_in_database = []

    def __init__(self):
        # self.logger = None
        self.session = None

    def create_logging(self):

        import logging

        self.logger = logging.getLogger(__name__)
        FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(asctime)s %(message)s"
        logging.basicConfig(format=FORMAT)

        # Create and configure logger
        # self.logging.basicConfig(filename="newfile.log", format='%(asctime)s %(message)s', filemode='w')

        # Creating an object
        self.logger = logging.getLogger()

        file_path = 'D:\\mycodes\\updated_fast_code\\get_all_csv_remove_chats_mongodb\\mylog.txt'
        open(file_path, 'w').close()
        fh = logging.FileHandler(file_path, 'w', 'utf-8')
        # fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        # Setting the threshold of logger to DEBUG
        self.logger.setLevel(logging.INFO)

        self.logger = logging.getLogger('')
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler(file_path)
        sh = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('[%(asctime)s] - %(funcName)s - %(message)s',
                                      datefmt='%a, %d %b %Y %H:%M:%S')
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(sh)

    def find_group_list(self):

        # group_resource_id="android:id/list"

        group_resource_id = "com.whatsapp:id/conversations_row_contact_name"

        # group_path="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.LinearLayout/android.widget.ListView/android.widget.RelativeLayout"
        # groups = self.driver.find_elements(by=AppiumBy.XPATH, value=group_path)
        groups = self.driver.find_elements(by=AppiumBy.ID, value=group_resource_id)
        # all_groups=groups.find_elements_by_xpath("./*")
        return groups

    contact_name_list = []

    def get_all_group_list(self):
        import random
        for x in range(0, 2):
            group_name_container_list = self.driver.find_elements(AppiumBy.ID, 'com.whatsapp:id/contact_row_container')
            random.shuffle(group_name_container_list)
            # el=group_name_container_list[0].find_element(AppiumBy.ID, 'com.whatsapp:id/conversations_row_contact_name')
            # group_name_container_list = self.driver.find_elements(AppiumBy.ID, 'com.whatsapp:id/conversations_row_contact_name')
            for group_name_container in group_name_container_list:
                try:

                    try:
                        group_name_element = group_name_container.find_element(AppiumBy.ID,
                                                                               'com.whatsapp:id/conversations_row_contact_name')
                        group_name = group_name_element.text
                        group_name = group_name.strip()
                        print(group_name)

                    except  Exception as e:
                        continue
                        pass

                    if group_name == step_02_last_group_name:
                        print("end of list ")
                        return "end of list"

                    myquery = {"_id": group_name}
                    records = wh.group_name_collection.find_one(myquery)

                    if records['Is_group_name_enable'] == False:
                        self.logger.info('this group is disable ===>    ' + group_name)
                        continue

                    result = self.go_inside_a_group(group_name_container, group_name)
                    if result == "exported":
                        self.contact_name.append(group_name)


                except Exception as e:
                    print(e)
                    pass

    def go_inside_a_group(self, group_name_element, group_name):

        if group_name == "Gulab Singhal One Day Press":
            print()

        try:
            is_already_scrap = self.find_group_already_Today_scrap_or_not(group_name)
            # is_already_scrap = self.find_group_already_Today_scrap_or_not(class_instance.id)
            if is_already_scrap == "yes":
                self.logger.info('already exported today ===>    ' + group_name)
                return "already_exported"

            if is_already_scrap == "no":
                start_time = time.time()
                group_name_element.click()
                time.sleep(5)
                result = self.check_group_empty_or_not(group_name)
                if result == "group_is_empty":
                    return "group_is_empty"
                full_group_name = self.find_full_group_name(group_name)
                if full_group_name == "person_contact":
                    return 'person_contact'
                self.logger.info('export csv   ' + full_group_name)
                if full_group_name == '':
                    return "not_found"
                self.save_csv_into_database(full_group_name, group_name, start_time)
                # self.driver.back()
                time.sleep(4)
                return "exported"
            if is_already_scrap == "not_found":
                return "not_found"
        except Exception as e:
            pass

    def search_group_button_get_element(self):
        "com.whatsapp:id/menuitem_search"
        serach_button_id = "com.whatsapp:id/menuitem_search"
        serach_button_element = self.driver.find_element(by=AppiumBy.ID, value=serach_button_id)
        # all_groups=groups.find_elements_by_xpath("./*")
        serach_button_element.click()
        # return serach_button_element

    def search_input_box_enter_group_name(self, group_name):
        serach_input = "com.whatsapp:id/search_input"
        serach_input_element = self.driver.find_element(by=AppiumBy.ID, value=serach_input)
        # all_groups=groups.find_elements_by_xpath("./*")
        group_name = str(group_name).replace("'", "").replace("'", "")
        self.logger.info("selecting group " + str(group_name))
        serach_input_element.set_text(group_name)
        time.sleep(2)
        # serach_input_element.click()
        # return serach_input_element

    def save_csv_into_database(self, full_group_full, group_name, start_time):
        try:
            # self.search_group_button_get_element()
            # self.search_input_box_enter_group_name(group_name)
            # self.driver.back()

            # self.result = self.enter_group_name_find_group_element(group_name)
            # if 'not found' in self.result:
            # self.update_group_found_details(self.session, class_instance.id, False)

            # print('this group not searchable please check spelling')
            # print
            # self.driver.back()
            # time.sleep(2)
            # continue
            # raise Exception

            self.collect_export_csv_file(full_group_full)

            # self.logger.info("left  " + str(total_group))
            # total_group = total_group - 1
            total_second = str(time.time() - start_time)
            self.logger.info("--- %s seconds ---" % (time.time() - start_time))
            # total_save_group = total_save_group + 1

            filde_data = self.get_exported_file_from_divice(full_group_full)

            if filde_data != "":
                # group_name_class=self.session.query(Group_name_table).filter(Group_name_table.Group_name == group_name).first()
                # self.session.query(Group_name_table).filter(Group_name_table.id == group_name_class.id).update({'Group_full_name': full_group_full})
                # self.session.commit()

                # add group full name into databse
                myquery = {"_id": group_name}
                newvalues = {"$set": {"Group_full_name": full_group_full}}

                wh.group_name_collection.update_one(myquery, newvalues)

                is_empty = False
                self.update_exported_table_details(total_second, group_name, group_name, filde_data, is_empty)

            else:
                myquery = {"_id": group_name}
                newvalues = {"$set": {"Is_group_name_enable": False, "csv_export": "error"}}

                wh.group_name_collection.update_one(myquery, newvalues)
                self.logger.info("exit from group")
                self.clean_mobile_whatsapp_text_folder()
                self.driver.back()

        except selenium.common.exceptions.InvalidSessionIdException as e:
            self.logger.error('A session is either terminated or not started')
            exit(0)
        except sqlalchemy.exc.PendingRollbackError as e:
            self.logger.error(e)
            self.session.rollback()
        except Exception as e:
            self.logger.error(e)
            self.driver.back()
            pass

    def check_group_empty_or_not(self, group_name):
        "com.whatsapp:id/conversation_row_date_divider"
        try:
            time.sleep(0.5)
            self.logger.info("check group empty or not")
            dots3_id = "com.whatsapp:id/conversation_row_date_divider"
            dots3 = self.driver.find_element(by=AppiumBy.ID, value=dots3_id)
            if dots3.text == "Today":
                group_name_class = self.session.query(Group_name_table).filter(
                    Group_name_table.Group_name == group_name).first()
                # self.session.query(Group_name_table).filter(Group_name_table.id == group_name_class.id).update(
                #    {'Group_full_name': "empty"})
                # self.session.commit()

                filde_data = b'empty'
                is_empty = True
                self.update_exported_table_details(10, group_name, group_name_class.id, filde_data, is_empty)
                self.driver.back()
                time.sleep(0.5)
                return "group_is_empty"

        except Exception as e:
            self.logger.error('this group is not empty')
            return "group_is_not_empty"

    def get_exported_file_from_divice(self, group_name):
        try:
            # group_name="MALIK JOBS GROUP ||"
            import shutil, os
            from pathlib import Path
            from subprocess import PIPE, run
            file_name = "WhatsApp Chat with " + group_name + ".txt"
            # com_str = subprocess.call("adb pull sdcard/" + file_name, shell=True)
            path = "sdcard/.aaaa/" + file_name
            # des_path=os.path.join(os.getcwd(), 'whatsapp_text_file')
            # des_path=Path().absolute().joinpath('whatsapp_text_file')
            # sor_path=os.path.join(os.getcwd(), file_name)
            # sor_path=Path().absolute().joinpath(file_name)

            # save_path=str(save_path)
            # for x in range(1,20):
            #     save_path=save_path.replace('\\\\','\\')
            # command = ['adb', 'pull',path,des_path]
            # result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            # print(result.returncode, result.stdout, result.stderr)

            file_base64 = self.driver.pull_file(path);
            # pick=myPickle()
            import base64
            # pick.storeObject(file_base64)
            mybytes = base64.b64decode(file_base64)
            if mybytes:
                return mybytes
            else:
                return False
        except Exception as e:
            # return False
            return ""
            # raise Exception

    def find_full_group_name(self, group_name):
        group_full_name = ""
        try:
            time.sleep(wait_time)
            self.logger.info("click on 3 dots")
            dots3_id = "com.whatsapp:id/menuitem_overflow"
            dots3 = self.driver.find_element(by=AppiumBy.ID, value=dots3_id)
            dots3.click()
            time.sleep((wait_time + 2))
        except Exception as e:
            self.logger.error('this group ' + group_name + ' not found in search result')
            return 'not found'

        try:
            self.logger.info("click on more")
            more_xpath = "//android.widget.TextView[@text='Group info']"
            dots3 = self.driver.find_element(by=AppiumBy.XPATH, value=more_xpath)
            dots3.click()
            time.sleep((wait_time + 2))
        except Exception as e:
            try:
                # check if this is group or person
                self.logger.info("click on View contact")
                more_xpath = "//android.widget.TextView[@text='View contact']"
                dots3 = self.driver.find_element(by=AppiumBy.XPATH, value=more_xpath)
                if dots3:
                    self.logger.info("this is person contact")

                    myquery = {"_id": group_name}

                    records = wh.group_name_collection.find(myquery)

                    # person=wh.session.query(Group_name_table).filter_by(Group_name=group_name).one()
                    try:

                        if records:
                            for record in records:
                                # myquery = {"Group_name": group_name}
                                # records = wh.group_name_collection.find(myquery).sort("group_name", -1)

                                myquery = {"_id": group_name}
                                newvalues = {"$set": {"Is_group_name_enable": False, "Group_type": "person"}}
                                wh.group_name_collection.update_one(myquery, newvalues)

                                print()
                        # self.session.query(Group_name_table).filter(Group_name_table.id == person.id).update(
                        #    {'Is_group_name_enable': False,"Group_type":"person"})
                        # self.session.commit()
                        self.driver.back()
                        time.sleep(2)
                        self.driver.back()
                        time.sleep(2)
                        return "person_contact"
                    except Exception as e:
                        pass
                # dots3.click()
                time.sleep((wait_time + 2))
            except Exception as e:
                myquery = {"_id": group_name}
                newvalues = {"$set": {"Is_group_name_enable": False, "Group_type": "error ingroup"}}
                wh.group_name_collection.update_one(myquery, newvalues)

                self.driver.back()
                self.logger.error('more not found' + str(e))

        try:
            self.logger.info("find ")
            more_xpath = "com.whatsapp:id/group_title"
            dots3 = self.driver.find_element(by=AppiumBy.ID, value=more_xpath)
            group_full_name = dots3.text
            print(group_full_name)
            # dots3.click()
            time.sleep((wait_time + 2))
        except Exception as e:
            self.logger.error('more not found')

        self.driver.back()
        return group_full_name

    def clear_group_chat_with_media(self, group_name):

        group_full_name = ""
        try:
            time.sleep(wait_time)
            self.logger.info("click on 3 dots")
            dots3_id = "com.whatsapp:id/menuitem_overflow"
            dots3 = self.driver.find_element(by=AppiumBy.ID, value=dots3_id)
            dots3.click()
            time.sleep((wait_time + 2))
        except Exception as e:
            self.logger.error('this group ' + group_name + ' not found in search result')
            return 'not found'

        try:
            self.logger.info("click on more")
            more_xpath = "//android.widget.TextView[@text='More']"
            dots3 = self.driver.find_element(by=AppiumBy.XPATH, value=more_xpath)
            dots3.click()
            time.sleep(wait_time)
        except Exception as e:
            self.logger.error('more not found')
            try:
                self.logger.info("click on more")
                more_xpath = "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[7]/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.TextView"
                dots3 = self.driver.find_element(by=AppiumBy.XPATH, value=more_xpath)
                dots3.click()
                time.sleep(wait_time)
            except Exception as e:
                self.logger.error('media not find')

        try:
            self.logger.info("click on Clear chat")
            export_chat_xpath = "//android.widget.TextView[@text='Clear chat']"
            dots3 = self.driver.find_element(by=AppiumBy.XPATH, value=export_chat_xpath)
            dots3.click()
            time.sleep(wait_time)
        except Exception as e:
            self.logger.error('this group ' + group_name + ' not found in search result')
            return 'not found'

        try:
            self.logger.info("click on clear chat button1")
            more_xpath = "android:id/button1"
            dots3 = self.driver.find_element(by=AppiumBy.ID, value=more_xpath)
            dots3.click()
            time.sleep((wait_time + 2))
        except Exception as e:
            self.logger.error('more not found' + str(e))

        # self.logger.info("exit from group")
        # self.driver.back()

    def collect_export_csv_file(self, group_name):
        wait_time = 2
        try:
            time.sleep(wait_time)
            self.logger.info("click on 3 dots")
            dots3_id = "com.whatsapp:id/menuitem_overflow"
            dots3 = self.driver.find_element(by=AppiumBy.ID, value=dots3_id)
            dots3.click()
            time.sleep(wait_time)
        except Exception as e:
            self.logger.error('this group ' + group_name + ' not found in search result')
            return 'not found'

        try:
            self.logger.info("click on more")
            more_xpath = "//android.widget.TextView[@text='More']"
            dots3 = self.driver.find_element(by=AppiumBy.XPATH, value=more_xpath)
            dots3.click()
            time.sleep(wait_time)
        except Exception as e:
            self.logger.error('more not found')
            try:
                self.logger.info("click on more")
                more_xpath = "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[7]/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.TextView"
                dots3 = self.driver.find_element(by=AppiumBy.XPATH, value=more_xpath)
                dots3.click()
                time.sleep(wait_time)
            except Exception as e:
                self.logger.error('media not find')

        try:
            self.logger.info("click on export chat")
            export_chat_xpath = "//android.widget.TextView[@text='Export chat']"
            dots3 = self.driver.find_element(by=AppiumBy.XPATH, value=export_chat_xpath)
            dots3.click()
            time.sleep(wait_time)
        except Exception as e:
            self.driver.back()
            time.sleep(wait_time)
            self.driver.back()
            time.sleep(wait_time)
            # self.driver.back()
            # time.sleep(wait_time)
            return 0
            pass

        try:
            self.logger.info("click on withot media")
            withot_media_xpath = "hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[6]/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.TextView"
            dots3 = self.driver.find_element(by=AppiumBy.XPATH, value=withot_media_xpath)
            dots3.click()
            time.sleep(wait_time)
        except Exception as e:
            self.logger.info('media not find')

        try:
            self.logger.info("click on withot media")
            withot_media_id = "android:id/button3"
            dots3 = self.driver.find_element(by=AppiumBy.ID, value=withot_media_id)
            dots3.click()
            time.sleep(wait_time)
        except Exception as e:
            self.logger.info('media not find')

        wait_for_element_visible = True

        while (wait_for_element_visible):
            try:

                # copy_to_xpath = "/1hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.GridView/android.widget.LinearLayout[4]/android.widget.TextView"
                # dots3 = self.driver.find_element(by=AppiumBy.XPATH, value=copy_to_xpath)
                # dots3.click()
                # wait_for_element_visible = False
                # time.sleep(1)

                # copy_to_xpath="//android.widget.TextView[@text='Copy to…']"
                copy_to_xpath = "//android.widget.TextView"
                # copy_to_xpath = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.GridView/android.widget.LinearLayout[4]/android.widget.TextView"
                all_options = self.driver.find_elements(by=AppiumBy.XPATH, value=copy_to_xpath)
                for option in all_options:
                    if "Copy to" in option.get_attribute("text"):
                        option.click()
                        # dots3.click()
                        wait_for_element_visible = False
                        time.sleep(2)
                        self.logger.info("click on copy_to")
                        time.sleep(2)
                        break
            except Exception as e:
                print(e)
                time.sleep(1)
                self.logger.error("waiting for finish process")

        try:
            # find .aaaa folder in file explorer
            aaa_folder_xpath = "//android.widget.TextView[@text='.aaaa']"
            dots3 = self.driver.find_element(by=AppiumBy.XPATH, value=aaa_folder_xpath)
            dots3.click()
            self.logger.info("click on .aaaa folder")
            time.sleep(wait_time)
        except Exception as e:
            pass

        self.logger.info("click on paste_botton")
        paste_botton_id = "com.mi.android.globalFileexplorer:id/paste_confirm"
        dots3 = self.driver.find_element(by=AppiumBy.ID, value=paste_botton_id)
        dots3.click()
        time.sleep(wait_time)
        try:
            self.logger.info("click on already_exist")
            already_exist_id = "android:id/button1"
            dots3 = self.driver.find_element(by=AppiumBy.ID, value=already_exist_id)
            dots3.click()
            time.sleep(wait_time)
        except Exception as e:
            self.logger.info('already no found')
        self.logger.info("exit .aaa folder")
        self.driver.back()
        time.sleep(wait_time)
        self.logger.info("exit fild manager")
        self.driver.back()
        time.sleep(wait_time)
        # self.logger.info("exit from group")
        # self.driver.back()
        # time.sleep(wait_time)

    def update_exported_table_details(self, total_second, group_name, group_name_id, filde_data, is_empty):
        import datetime
        try:
            # ct = datetime.datetime.now()
            file_name = "WhatsApp Chat with Indian Jobs.txt"
            file_name = "WhatsApp Chat with " + group_name + ".txt"
            if is_empty == True:
                file_name = "blank"
            # try:
            #     import base64
            #     filde_data_binary = base64.decodebytes(filde_data)
            # except Exception as e:
            #     pass

            fild_size = len(filde_data)
            # group_txt_export_class = Group_Txt_Export(Group_name=group_name,Group_export_process_time=total_second,
            #                                          Group_export_file_name=file_name,group_name_id=group_name_id,
            #                                          Group_export_data_file=filde_data,Group_export_txt_file_size=fild_size)

            ct = datetime.datetime.now()
            Group_export_dataTime = ct
            total_second = round(float(total_second))
            group_txt_export_class = {'Group_name': group_name, 'Group_export_process_time': total_second,
                                      'Group_export_file_copy_system': 'yes',
                                      'Group_export_dataTime': Group_export_dataTime,
                                      'Group_export_file_name': file_name, 'group_name_id': group_name_id,
                                      'Group_export_data_file': filde_data, 'Group_export_txt_file_size': fild_size,
                                      'Group_export_file_convert_to_csv': 'no',
                                      'Group_export_file_csv_upload_in_db': 'no', 'Group_export_csv_file': None}

            # records = self.session.query(Group_name).filter_by(Group_name=group_name).all()
            # if len(records) == 0:

            wh.group_txt_export_collection.insert_one(group_txt_export_class)
            # self.session.add(group_txt_export_class)
            # self.session.commit()
            # self.session.

            # group_txt_export_class.printclass()

            # print(group_name_class)
            # print(group_name_class.Group_name)
            # total_save_group = total_save_group + 1
            # else:
            # pass
            # total_save_group_aready_in_database = total_save_group_aready_in_database + 1

            if is_empty == False:
                # pass
                # self.clear_group_chat_with_media(group_name)
                self.logger.info("exit from group")
                self.clean_mobile_whatsapp_text_folder()
                self.driver.back()

        except sqlalchemy.exc.IntegrityError as e:
            self.session.rollback()
        except Exception as e:
            self.logger.error(e)
            pass
            # self.session.rollback()

    def myscroll_bottom_to_top(self):

        loop = True
        while (loop):
            try:
                result = self.get_all_group_list()
                self.scroll_down()
                if result == "end of list":
                    loop = False

            except selenium.common.exceptions.InvalidSessionIdException as e:
                print('A session is either terminated or not started')
                exit(0)

            except Exception as e:
                pass
            # find last element
            # try:
            # reach_last=self.driver.find_element(AppiumBy.ID,'com.whatsapp:id/conversations_row_tip_tv')
            # if reach_last:
            # loop=False
            # break
            # except Exception as e:
            # pass
        pass

    def find_group_already_Today_scrap_or_not(self, group_name):

        try:
            # group_name_class=any
            try:

                if group_name.startswith("+"):
                    print("this is not a group " + str(group_name))
                    raise Exception

                myquery = {"_id": group_name}

                group_name_class = wh.group_name_collection.find_one(myquery)
                # group_name_class=self.session.query(Group_name_table).filter_by(Group_name=group_name).one()
            except Exception as e:
                myquery = {"Group_full_name": group_name}

                group_name_class = wh.group_name_collection.find_one(myquery)

                # group_name_class = self.session.query(Group_name_table).filter_by(Group_full_name=group_name).one()

            if group_name_class['Is_group_name_enable'] == False:
                self.logger.info("this is group disable " + str(group_name))
                is_already_scrap = "group_disable"
                return is_already_scrap

            # records = self.session.query(Group_Txt_Export).filter_by(group_name_id=group_name_class.id).all()

            # records=self.session.query(Group_Txt_Export).filter_by(group_name_id=group_name_class.id).order_by(
            #    Group_Txt_Export.Group_export_dataTime.desc()).all()
            myquery = {"Group_name": group_name}

            records = wh.group_txt_export_collection.find(myquery).sort("Group_export_dataTime", -1)
            # records=[]
            is_already_scrap = False
            import datetime;
            avalable_data = 0
            if records:
                # from operator import attrgetter
                # sorted_list = sorted(records, key=attrgetter('Group_export_dataTime'))
                # reversed(sorted_list)
                for record in records:
                    avalable_data = avalable_data + 2
                    ct = datetime.datetime.now()
                    date = record['Group_export_dataTime']
                    if ct.date() == date.date():
                        is_scrap = record['Group_export_file_copy_system']
                        if is_scrap == "yes":
                            is_already_scrap = "yes"
                            return is_already_scrap
                        if is_scrap == "no":
                            is_already_scrap = "no"
                            return is_already_scrap
                    if ct.date() != date.date():
                        is_scrap = record['Group_export_file_copy_system']
                        if is_scrap == "yes":
                            is_already_scrap = "no"
                            return is_already_scrap
                        if is_scrap == "no":
                            is_already_scrap = "no"
                            return is_already_scrap

            if avalable_data == 0:
                self.logger.info("no record found in export  data table" + str(group_name))
                is_already_scrap = "no"
                return is_already_scrap

        except Exception as e:

            print("group name not found in database  " + str(group_name))
            print(e)
            self.group_not_found_in_database.append(group_name)
            return "not_found"

    def scroll_up(self):
        self._y_scroll(self.scroll_y_top, self.scroll_y_bottom)

    def scroll_down(self):
        window_size = self.driver.get_window_size()
        self.scroll_y_top = window_size['height'] * 0.2
        self.scroll_y_bottom = window_size['height'] * 0.8
        self.scroll_x = window_size['width'] * 0.5
        self._y_scroll(self.scroll_y_bottom, self.scroll_y_top)

        try:
            selected_element = self.driver.find_element(AppiumBy.ID, 'com.whatsapp:id/action_mode_close_button')
            if selected_element:
                self.driver.back()
        except  Exception as e:
            pass

    def _y_scroll(self, y_start, y_end):
        try:
            SCROLL_DUR_MS = 1000
            actions = TouchAction(self.driver)
            actions.long_press(None, self.scroll_x, y_start, SCROLL_DUR_MS)
            actions.move_to(None, self.scroll_x, y_end)
            actions.release()
            actions.perform()
        except Exception as e:
            self.reluanch()

        # actions.wait(1000)
        # actions.press(None, self.scroll_x, y_end, SCROLL_DUR_MS)
        # actions.perform()
        # self.driver.back()

    def clean_filter_upload_in_db(self):
        print('start filtering group list')
        contact_name_list = self.contact_name
        # contact_name_list=['MALIK JOBS GROUP ||', 'infoITLeads #1', '+91 98592 00200', 'Mywork', 'Indian Jobs', 'Anil Engineer', 'Infosys Digital Xperience', 'BAG-1 July 2021 G-4', 'Anil Engineer', 'Infosys Digital Xperience', 'BAG-1 July 2021 G-4', 'युवा धार्मिक मंच 🙏🙏🙏', 'Spring Boot- ERP project', 'Gulab Singhal One Day Press', 'Bheem Mourya Mukand Pur Juice Shop', '+91 98890 37270', '+91 72044 74413', 'Spring Boot Dev Bangalore', 'Bheem Mourya Mukand Pur Juice Shop', '+91 98890 37270', '+91 72044 74413', 'Spring Boot Dev Bangalore', 'CSC North east Delhi 2', 'Papa', '+91 70653 63830', 'AADHAAR CENTER PROVIDER N', '+91 98114 73027', '+91 97291 77820', 'AADHAAR CENTER PROVIDER N', '+91 98114 73027', '+91 97291 77820', 'Lakhi Ram. Bharola Pan Client', 'IndusInd Bank', 'Dr Vinod Vinod', '+92 324 7959281', 'JavaOnFly', '+44 7423 307331', 'Milaap', '+92 324 7959281', 'JavaOnFly', '+44 7423 307331', 'Milaap', '+91 99100 41807', 'Dheeraj', '+91 79950 25077', 'Python Project ', '+880 1876-320043', 'ETrade Project', 'Python Project ', '+880 1876-320043', 'ETrade Project', 'Neelam Rai', 'North West Delhi VLEs', 'Ashok IT - 102', '+91 96660 69069', 'Pankaj Chaudhary', '+234 806 570 4147', '+91 96660 69069', 'Pankaj Chaudhary', '+234 806 570 4147', '+1 (312) 399-7112', '+243 821 594 129', '+91 85128 80093', 'Subodh Sinha', 'KINGDOM CROWN MULTISERVIC', '+91 97390 56067', '+919212300704', 'KINGDOM CROWN MULTISERVIC', '+91 97390 56067', '+919212300704', '+91 99587 80625', '+1 (857) 488-4693', '+91 72908 54453', 'Programming Freelance', '+91 99900 48361', '+91 88827 03418', 'Programming Freelance', '+91 99900 48361', '+91 88827 03418', '+1 (617) 304-4212', '+92 308 0005009', 'Freind', '+91 6295 268 646', '+91 72959 93806', '+92 303 8253251', '+91 83368 64964', '+91 6295 268 646', '+91 72959 93806', '+92 303 8253251', '+91 83368 64964', '+1 (541) 636-8040', '+91 88022 42025', '+91 84479 74015', '+91 98117 04999', '+91 85002 27070', 'Adharcard update center i', '+91 98117 04999', '+91 85002 27070', 'Adharcard update center i', '+91 72177 19038', '+91 96437 46561', 'Tarun Chaudhary Adv', 'Group DevOps 2', '+91 70115 38373', '+91 97738 46437', 'Group DevOps 2', '+91 70115 38373', '+91 97738 46437', '+91 93506 57668', 'Java Training & Placement', '+91 82872 42633', 'Anu Student', '+91 11 4010 4241', 'Earn work from home', 'Milaap Social Ventures', 'Anu Student', '+91 11 4010 4241', 'Earn work from home', 'Milaap Social Ventures', 'K.s.sharma.v', '+91 95138 79610', 'Manju Anil Bhabhi', '+91 92150 00714', '+91 99118 58184', 'T CSC North Delhi Group👍', '+91 92150 00714', '+91 99118 58184', 'T CSC North Delhi Group👍', '+91 78400 14229', '+91 75438 00768', 'Pankaj Wife Gunja Kumari Mukand Pur', '+91 80103 54151', 'Prabhu Din', '+91 6232 107 818', '+91 89290 45571', '+91 80103 54151', 'Prabhu Din', '+91 6232 107 818', '+91 89290 45571', 'Dr Vinod Vinod', 'Ram Lal Azadpur', 'Master Pay Uncle', '+91 85278 94842', '+92 317 6651743', '+91 72102 86986', '+91 85278 94842', '+92 317 6651743', '+91 72102 86986', '+91 81794 42979', '🙏', 'Shekhar Singh Csc', '+91 99608 41818', 'Rishab Jp', 'Prime Cash pro', '+91 99608 41818', 'Rishab Jp', 'Prime Cash pro', '+91 99103 20639', '+91 98104 31695', 'Annu Rohini Court Fake', '+234 813 869 7519', '+91 80738 38283', 'Ig follower error solve ', 'Rksingh Raghav Paras Milk', '+234 813 869 7519', '+91 80738 38283', 'Ig follower error solve ', 'Rksingh Raghav Paras Milk', 'Raju yadav', 'Sanjay Adhar Test', '+91 84480 12238', '+91 87509 10449', 'Tech Work', '+91 80106 48684', '+91 87509 10449', 'Tech Work', '+91 80106 48684', 'DEV Freelance Team 2', 'MODICARE', '+91 95286 18971', '+91 89192 32014', 'Adv Rajkumar Singh', '+91 96252 82394', '+91 89192 32014', 'Adv Rajkumar Singh', '+91 96252 82394', 'Tata Play', '+91 80111 12020', 'Csp banking group', 'TAXOLOGIST', '+91 93192 64482', '+91 99117 51486', '+91 81025 12692', 'TAXOLOGIST', '+91 93192 64482', '+91 99117 51486', '+91 81025 12692', '+91 73409 02187', '+91 77229 50122', '+91 99998 80084', 'tayalprince2020', '+91 95128 88220', '+91 95607 63782', 'tayalprince2020', '+91 95128 88220', '+91 95607 63782', '+91 93152 33884', '+91 91747 59728', '+91 88806 78910', '+91 88718 33347', 'Jio Offers', '+1 (405) 835-6738', '...ask', '+91 88718 33347', 'Jio Offers', '+1 (405) 835-6738', '...ask', '+91 92105 69496', '+91 91087 18827', '+91 85279 49330', '+91 81019 24661', '+91 80763 93536', '+880 1773-759895', '+91 81019 24661', '+91 80763 93536', '+880 1773-759895', '+91 95823 60537', '+91 84868 88533', '+91 99885 82146', '+91 81302 65994', 'Manoj Rajput', '+91 74284 79391', '+91 81302 65994', 'Manoj Rajput', '+91 74284 79391', '+91 99602 88847', 'Sir', 'Temp Cyber Cafe Andaz', '+91 98731 11792', '+91 93551 78191', '+91 91318 57705', '+91 80761 06713', '+91 98731 11792', '+91 93551 78191', '+91 91318 57705', '+91 80761 06713', '+91 97185 55395', 'General Discussion', 'Swiggy group', 'Aadhar Card bhai', 'Brij Krishna Customer', 'BTC wealth 051', 'Aadhar Card bhai', 'Brij Krishna Customer', 'BTC wealth 051', '+91 93102 36015', 'Fino Payments Bank', '+91 98117 14482', 'MODICARE ', 'Arvind motheboard', '+250 723 993 376', 'MODICARE ', 'Arvind motheboard', '+250 723 993 376', '+91 95826 03404', 'Pankaj Mukanadpur', '+91 93130 75637', '+91 98183 92001', '+250 783 982 872', '+91 84482 52839', 'Pawan Bharti', '+250 783 982 872', '+91 84482 52839', 'Pawan Bharti', '+91 92898 29872', '+91 88515 95676', '+91 77699 45320', '+968 9277 2429', '+91 83898 84818', 'Abhisek Ducat', '+968 9277 2429', '+91 83898 84818', 'Abhisek Ducat', 'Poonam Verma', '+91 84482 39760', '+91 91772 36253', '+91 78811 84184', '+91 97030 80696', '+91 83490 70650', '+91 99362 09520', '+91 78811 84184', '+91 97030 80696', '+91 83490 70650', '+91 99362 09520', '+91 78720 27047', '+91 96409 64045', '+91 92122 59595', '+353 83 033 2685', '+91 6358 736 660', 'Print Out Rohini Courts', '+353 83 033 2685', '+91 6358 736 660', 'Print Out Rohini Courts', 'Java Express Updates 2020', '+91 98188 75152', 'Mohan Lal Chauhan Lic', 'Annu Ansari Epfo', 'Vikash Adv', 'Santosh', '+91 78388 25007', 'Annu Ansari Epfo', 'Vikash Adv', 'Santosh', '+91 78388 25007', '+91 99003 27273', 'Ndee C। Temp Test Customers', 'Anand Professional Courier', 'Dipa Di Moni Sister Pan Customer', '+91 98119 55910', '+91 93119 04276', 'Dipa Di Moni Sister Pan Customer', '+91 98119 55910', '+91 93119 04276', '+91 95997 17121', 'Mannu Kumar Vle', '+91 73030 64253', 'Atul Ducat', 'Patel Test Pan Customer Bhrola Lakhi Ram', '+91 99357 74312', '+91 99118 86181', 'Atul Ducat', 'Patel Test Pan Customer Bhrola Lakhi Ram', '+91 99357 74312', '+91 99118 86181', 'Rajesh Osho', '+91 91363 50649', 'Pandit Ji Mukandpur Hdfc Atm', '+91 98994 75185', '.', 'Pandit Ji Mukandpur Hdfc Atm', '+91 98994 75185', '.', '+91 92892 43226', 'Zoom', 'Monu Advocate', '+91 93102 17449', '+91 98109 81750', 'Surendra Sharma Tution', 'Sunil Yadav Online', '+91 98109 81750', 'Surendra Sharma Tution', 'Sunil Yadav Online', '+91 92892 69715', 'Pushpa Naagar', 'abhisek _java', 'Md Meraj Alam Customer', 'Rupesh Salaiya', 'CSP Csc adhar corection g', 'Md Meraj Alam Customer', 'Rupesh Salaiya', 'CSP Csc adhar corection g', '+91 88828 85655', 'Ronit Roy Misra Mukand Pur', '+91 85955 13508', '+91 99119 02109', '+91 6283 192 009', '+91 98680 99890', '+91 80592 95153', '+91 99119 02109', '+91 6283 192 009', '+91 98680 99890', '+91 80592 95153', '+91 73595 59259', '+91 99316 48501', '+91 99905 37694', '+91 98210 41931', 'Fino Faimily Mukundpur🥢🥢🥢', '+91 85058 61333', '+91 98210 41931', 'Fino Faimily Mukundpur🥢🥢🥢', '+91 85058 61333', 'Deepak Ji Yuva Dharmik Manch Mukandpur', '+91 97189 52262', '+91 86970 66800', 'Good Luck Vinod', 'CSC North delhi top 2020 vle', '+91 95403 68065', '+91 92111 79211', 'Good Luck Vinod', 'CSC North delhi top 2020 vle', '+91 95403 68065', '+91 92111 79211', 'Kalyan Singh Rawat Save', 'Manoj Rathor Customer', '+91 85217 77262', '+91 95820 40170', 'Utilities Point Csc', '+91 88008 23608', '+91 95820 40170', 'Utilities Point Csc', '+91 88008 23608', 'Kajal Kumari', '+91 99994 50338', '+91 98914 75767', '+91 76040 50925', '+91 70119 73787', 'Vijay Kumar Customer', 'North Delhi VLE', '+91 76040 50925', '+91 70119 73787', 'Vijay Kumar Customer', 'North Delhi VLE', '+91 79825 11441', '+91 93116 68423', '+91 70424 70511', '+91 92100 18017', '+91 86003 70573', '+91 85120 37447', '+91 92100 18017', '+91 86003 70573', '+91 85120 37447', '+91 77019 77937', '+91 87997 24701', '+91 91134 62177', '+91 98735 33105', 'Mukesh Pal Mukand Pur Office Gali', 'Sandeep Pal Pan Client', '+91 98735 33105', 'Mukesh Pal Mukand Pur Office Gali', 'Sandeep Pal Pan Client', '+91 85956 31844', 'Sonu Sharma R K Sharma Advocate Associate', 'Sanjay Adhaar Card Maker', 'Hirdesh Kumar Student', '+91 90696 95383', '+91 74402 92188', 'Pinky Herbel Life Mukandpur', 'Hirdesh Kumar Student', '+91 90696 95383', '+91 74402 92188', 'Pinky Herbel Life Mukandpur', '+91 88094 35095', '+91 98739 83605', '+91 85954 24304', '+91 88267 01253', '+91 75182 92007', '+91 98716 48296', '+91 88267 01253', '+91 75182 92007', '+91 98716 48296', '+91 70653 59144', '+91 78279 61810', '+91 93152 22546', '+91 74289 49381', '+91 93112 83603', 'Pooja Bhati Temp Customer', '+91 85951 59882', '+91 74289 49381', '+91 93112 83603', 'Pooja Bhati Temp Customer', '+91 85951 59882', '+91 85275 62981', '+91 82854 88730', 'Anil Sangwan Police Bhalaswa Thana', '+91 84340 42199', '+91 87770 15855', 'Harikesh Kumar Customer Mukand Pur', '+91 84340 42199', '+91 87770 15855', 'Harikesh Kumar Customer Mukand Pur', 'Uber', '+91 78560 07344', 'Dahiya Sahab Mcd', 'Deepak Saleem Loan', '+91 70656 55543', '+91 74393 23131', 'Deepak Saleem Loan', '+91 70656 55543', '+91 74393 23131', '+91 87997 27560', '+91 96543 62974', '+91 98990 89539', '+91 78380 26665', '+91 85879 22535', '+91 88102 95137', '+91 78380 26665', '+91 85879 22535', '+91 88102 95137', '+91 79823 69671', '+91 87429 72489', '+91 76781 75833', '+91 95402 23474', '+91 81786 40651', '+91 93192 74755', '+91 75250 03100', '+91 95402 23474', '+91 81786 40651', '+91 93192 74755', '+91 75250 03100', 'Ramesh Mukand Pur Vinod', 'Aashu Singh Customer Surjan Singh Dda Application', '+91 95511 42000', '+91 93526 49861', '+91 93136 37350', '+91 85879 61767', '+91 93526 49861', '+91 93136 37350', '+91 85879 61767', '+91 92784 90825', 'Bandhu Thakur Whatsapp Customer', '+91 93118 34624', '+91 98101 09599', '+91 78276 29404', '+91 97919 51433', '+91 99284 09163', '+91 98101 09599', '+91 78276 29404', '+91 97919 51433', '+91 99284 09163', 'Rahul Paytm Kyc', 'Rajesh Chohan Ji Bhalsva Riksha', '+91 820 951 2982', 'Dr Mahesh Pal Mukand Pur', 'God is good', '+91 87507 39553', '+91 820 951 2982', 'Dr Mahesh Pal Mukand Pur', 'God is good', '+91 87507 39553', '+91 98737 90745', '+91 85889 08274', '+91 88105 78307', '+91 88607 80373', 'Radhanandan Thakur Customer', '+91 78509 13745', '+91 88607 80373', 'Radhanandan Thakur Customer', '+91 78509 13745', '+91 98914 74857', '+91 95401 37378', '+91 89208 69091', '+91 78271 91508', '+91 87505 42331', '+91 78275 71602', '+91 79825 08422', '+91 78271 91508', '+91 87505 42331', '+91 78275 71602', '+91 79825 08422', '+91 99904 95529', 'Madan Kumar Customer', '+91 99908 60629', '+91 86010 40188', '+91 99110 39514', '+91 99901 24301', '+91 99908 60629', '+91 86010 40188', '+91 99110 39514', '+91 99901 24301', 'Payworld', '+91 78383 66730', '+91 97189 70098', '+91 93155 28271', '+91 98189 32744', '+91 78271 50112', '+91 93155 28271', '+91 98189 32744', '+91 78271 50112', 'Sanjay Jio', '+91 83681 32644', '+91 85276 45157', '+91 83682 88780', '+91 89202 40013', '+91 70821 59181', 'Niharika Chawla Adrash Nagar Chawal Uncle', '+91 83682 88780', '+91 89202 40013', '+91 70821 59181', 'Niharika Chawla Adrash Nagar Chawal Uncle', '+91 79820 14367', '+91 70654 34418', 'Pankaj Kumar Customer', '+91 92679 63458', '+91 99903 36059', '+91 99530 57760', '+91 92679 63458', '+91 99903 36059', '+91 99530 57760', '+91 85068 87652', '+91 88106 16887', 'Deva Lal Bagh Degital Service', '+91 82714 52182', '+91 83840 13428', '+91 85953 38719', '+91 82714 52182', '+91 83840 13428', '+91 85953 38719', 'Yashwant Singh Khalli Mukand Pur', '+91 84483 54850', 'Deepak Kumar Customer', 'Prem Dp Bhadola', '+91 85870 47002', '+91 98919 97246', '+91 93545 40372', 'Prem Dp Bhadola', '+91 85870 47002', '+91 98919 97246', '+91 93545 40372', 'Santosh Panday Book Binding', 'Rajesh Chatbale Shaadi Test', 'Ashish Choubey Customer', '+91 96676 56554', '+91 98181 92820', 'Bhumesh Tumu Dilhi Payment Bank UCL Csc', '+91 96676 56554', '+91 98181 92820', 'Bhumesh Tumu Dilhi Payment Bank UCL Csc', '+91 95557 63808', 'Shahid Khan Pan Customer Temp', '+91 85273 09241', 'HDFC Bank Ltd', '+91 88269 02464', '+91 98116 77426', '+91 89726 94994', 'HDFC Bank Ltd', '+91 88269 02464', '+91 98116 77426', '+91 89726 94994', 'Mukesh Customer Pan', '+91 90652 75548', 'Manish Kumar Student', 'Vipin Jatav Customer', '+91 76781 25170', '+91 77798 99413', 'Vipin Jatav Customer', '+91 76781 25170', '+91 77798 99413', '+91 89206 88410', 'Anita Soni Test Shaadi. Com', 'Bhabani Test Shaadi. com', 'Pardip Kotpuli Neelam', '+91 88848 03030', '+91 92136 13082', 'Pardip Kotpuli Neelam', '+91 88848 03030', '+91 92136 13082', '+91 80101 95649', '+91 70612 37307', '+91 96649 80182', 'Ram Bahadur. Money', '+91 97186 90599', '+91 88514 34843', '+91 95556 77731', 'Ram Bahadur. Money', '+91 97186 90599', '+91 88514 34843', '+91 95556 77731', 'Kanishk Jayswal Customer', '+91 90505 11506', '+91 93153 13866', 'Pooja Bhati Test Shaadi. com', '+91 95998 68148', 'Akansha Pandey Test Shaadi. Com', 'Pooja Bhati Test Shaadi. com', '+91 95998 68148', 'Akansha Pandey Test Shaadi. Com', '+91 98913 94953', 'Zomato legal', 'OYO', '+91 81304 49719', '+91 82874 34282', 'Ramesh Sahu Mp', '+91 97186 27511', '+91 81304 49719', '+91 82874 34282', 'Ramesh Sahu Mp', '+91 97186 27511', 'Parveen Gupta Loan Mukand Pur', '+91 89796 91501', 'Utkarsh Verma Sbi Csp', '+91 97180 41893', 'Swati Chopra Test Shaadi. Com', 'Rahul Bharola Kumar', '+91 97180 41893', 'Swati Chopra Test Shaadi. Com', 'Rahul Bharola Kumar', 'Gaurav Mg Customer', 'Pooja Singh Shaadi Test 1 Children', 'Amit Ji Azadpur', '+91 83077 89631', 'Bablu Singh Uber', 'Shivam Electrition Customer', '+91 83077 89631', 'Bablu Singh Uber', 'Shivam Electrition Customer', 'Pawan Electronics Muk', 'Sangita @', 'Mittu Shaadi Test', 'Prem Sharma Photo Studio', '+91 75686 84501', 'Vinay Bord Customer', 'Onkar', 'Prem Sharma Photo Studio', '+91 75686 84501', 'Vinay Bord Customer', 'Onkar', "Saprinder Kaur Omkar's Wife", 'SIFF Temp Group-No Spam', '+91 88002 89472', '+91 75450 54000', 'Cardiology', 'manoj chauhan', '+91 75450 54000', 'Cardiology', 'manoj chauhan', 'Amit Survey', 'Sarthak Jain Dda Surveyor', '+91 70870 31479', 'Krishan Mukandpur', 'Op', '+91 93550 24409', '+91 96084 40548', 'Krishan Mukandpur', 'Op', '+91 93550 24409', '+91 96084 40548', 'Kapoor Singh Mukand Pur', 'Chandan Pandey', 'Corona Chat Bot Kejeriwal Delhi', 'OYO Hotels & Homes', 'Amit Paswan Gali', '+91 84530 00450', 'OYO Hotels & Homes', 'Amit Paswan Gali', '+91 84530 00450', 'Rajesh Rai Rai', '+91 88963 38921', '+91 96438 87339', 'Anil Ji', '+91 74285 92813', '+91 96545 43772', 'Anil Ji', '+91 74285 92813', '+91 96545 43772', 'Zomato', 'Aadhar update center', '+91 84470 98008', '+91 84477 20780', '+91 93343 83422', 'Tittoo', '+91 79823 08129', '+91 84477 20780', '+91 93343 83422', 'Tittoo', '+91 79823 08129', '+91 78348 51676', 'Icici Direct Whatsapp', '+91 99530 44604', '+91 99530 01977', '+91 84470 39089', '+91 98719 76909', '+91 99530 01977', '+91 84470 39089', '+91 98719 76909', '+91 78274 34963', '+91 98822 82615', '+91 86979 33289', '+91 83758 81641', 'Rakesh Kumar Saini Pan', '+91 87505 16399', '+91 78383 58761', '+91 83758 81641', 'Rakesh Kumar Saini Pan', '+91 87505 16399', '+91 78383 58761', 'Sunil Kumar DDA Survey', 'Sunny Dhiman Uber', '+91 76783 93320', '+91 99116 33614', '+91 99103 52094', '+91 88608 08917', '+91 99116 33614', '+91 99103 52094', '+91 88608 08917', '+91 99719 75355', 'Fashion@Discount', '+91 70116 57833', 'Shyam Sunder Lic Loan', '+91 81781 63988', 'Ravi Kumar Swiggy', 'Shyam Sunder Lic Loan', '+91 81781 63988', 'Ravi Kumar Swiggy', '+91 98731 00738', 'Ram Sharma Jahgirpuri K BLOCK REMESH FRIEND', '+91 83568 42904', '+91 88820 13743', '+91 83568 42870', 'CSC Enum ECI 2019', 'Kashif Uber', '+91 88820 13743', '+91 83568 42870', 'CSC Enum ECI 2019', 'Kashif Uber', 'Sanjay', 'Hero', '+91 88601 88219', '+91 97180 19550', '+91 99997 28464', '+91 88020 43840', '+91 97180 19550', '+91 99997 28464', '+91 88020 43840', '+91 98919 52314', '+91 96543 48778', '+91 99110 63673', '+91 83750 71946', '+91 88605 11897', '+91 92139 27746', 'Awadhesh Sir J Pan Client', '+91 83750 71946', '+91 88605 11897', '+91 92139 27746', 'Awadhesh Sir J Pan Client', 'Zomato strike', '+91 98995 18568', 'style.com', '+91 97160 72029', '+91 88512 61774', '+91 97110 39914', '+91 97160 72029', '+91 88512 61774', '+91 97110 39914', '+91 98112 82921', '+91 98704 60069', '+91 82290 83122', '+91 88007 02185', '+91 96714 80845', 'Rakesh Bharatwaj Zemoto', '+91 88007 02185', '+91 96714 80845', 'Rakesh Bharatwaj Zemoto', '+91 98102 34939', '+91 97165 99598', '+91 80763 61525', '+91 85278 20470', '+91 87500 71261', '+91 89208 18233', '+91 82850 46814', '+91 85278 20470', '+91 87500 71261', '+91 89208 18233', '+91 82850 46814', 'Anuj Ajazpur', '+91 99908 05374', '+91 84472 07031', '+91 78381 89939', '+91 98688 79140', '+91 95600 43185', '+91 78381 89939', '+91 98688 79140', '+91 95600 43185', '+91 95400 92131', '+91 88260 65667', 'Jyoti Kumari Stu', '+91 79823 02454', 'Dheeraj Uber', '+91 72668 70088', 'Mamta Shalot', '+91 79823 02454', 'Dheeraj Uber', '+91 72668 70088', 'Mamta Shalot', '+92 346 3196744', '+91 81410 08843', '+91 95604 66149', '+91 89296 59580', '+91 94639 20674', '+91 80102 96897', '+91 89296 59580', '+91 94639 20674', '+91 80102 96897', '+91 95823 05145', 'Sonu Kumar Zamoto Tl', '+91 98119 26587', '+91 80762 86662', 'Subash Meena Police', '+91 94513 10620', '+91 82964 72674', '+91 80762 86662', 'Subash Meena Police', '+91 94513 10620', '+91 82964 72674', '+91 6360 354 389', 'Gautam Kumar Paytm Agent Mukandpur', '+91 80101 04745', 'Vinod Kumar Zemoto', '+91 75318 82661', '+91 99901 25598', 'Vinod Kumar Zemoto', '+91 75318 82661', '+91 99901 25598', '+91 99992 87436', '+91 98993 12535', '+91 95107 55639', '+91 99586 07773', '+91 98182 26182', '+91 85889 30082', '+91 99586 07773', '+91 98182 26182', '+91 85889 30082', '+91 97110 67373', '+91 99107 40372', '+91 93548 09906', '+91 97189 46593', 'Paramveer Singh Zomato', '+91 95107 50293', '+91 97115 11688', '+91 97189 46593', 'Paramveer Singh Zomato', '+91 95107 50293', '+91 97115 11688', 'Deepak Gulati Zamoto', '+91 78278 58595', '+91 87003 52178', '+91 93132 23344', '+91 93551 56801', 'Amarjeet Pan Client Panchwati', '+91 93132 23344', '+91 93551 56801', 'Amarjeet Pan Client Panchwati', '+91 98177 77721', '+91 88106 70295', 'Aashish Panwar Loan Indiabulls', '+91 96504 93835', '+91 95606 29037', '+91 85272 60318', '+91 84477 92784', '+91 96504 93835', '+91 95606 29037', '+91 85272 60318', '+91 84477 92784', 'Narender Bisht. Ubar Eats', 'Sandeep Kumar Bike', '+91 75230 27244', '+91 78273 99418', '+91 80 10 931906', '+91 99990 59130', '+91 75230 27244', '+91 78273 99418', '+91 80 10 931906', '+91 99990 59130', '+91 98105 82576', '+91 96255 61997', '+91 81308 13383', '+91 70658 57418', 'Gopal Roy Pan Client', '+91 70652 23774', '+91 70658 57418', 'Gopal Roy Pan Client', '+91 70652 23774', '+91 98105 01399', '+91 99904 49663', 'Krishna Jeet Test Shaadi. com', '+91 98997 09513', '+91 78791 21784', 'Uday Raj Chaurasiya', '+91 95822 06333', '+91 98997 09513', '+91 78791 21784', 'Uday Raj Chaurasiya', '+91 95822 06333', '+91 98739 87410', '+91 91363 79371', '+91 95402 35387', '+91 91409 46756', '+91 83682 41894', '+91 88009 52839', '+91 95402 35387', '+91 91409 46756', '+91 83682 41894', '+91 88009 52839', 'Mannu Boyer Internet', 'Anil beta', 'Roshan Prasad Client Mukand pur', '+91 92050 62571', '+91 84198 76641', '+91 92134 01498', '+91 92050 62571', '+91 84198 76641', '+91 92134 01498', '+91 80766 80442', '+91 90650 77044', '+91 70118 13415', '+91 93193 25051', 'Rishi Test Shaadi. com', 'Rajni Gulliya Test Shaadi. com', '+91 75055 45556', '+91 93193 25051', 'Rishi Test Shaadi. com', 'Rajni Gulliya Test Shaadi. com', '+91 75055 45556', 'Ruchi Casper Mico Credit Test Shaadi. com', '+91 96504 58319', '+91 84620 59222', '+91 6303 436 220', '+91 95607 63807', '+91 97171 24298', '+91 6303 436 220', '+91 95607 63807', '+91 97171 24298', 'Vinod Kiran Pan Card', '+91 96545 56619', 'Neha Shaadi. Com Test Temp', '+91 98107 75984', 'Rana Ji Rana Test Shaadi', '+91 97188 70623', '+91 98107 75984', 'Rana Ji Rana Test Shaadi', '+91 97188 70623', '+91 96169 95929', '+91 98215 46030', 'Dabloo Sonkar Student', '+91 88396 23445', '+91 92896 52032', '+91 88717 19292', 'Amar Jeet', '+91 92896 52032', '+91 88717 19292', 'Amar Jeet', '+91 99539 16697', '+91 98731 38468', '+91 85307 55557', '+91 98714 17579', '+91 93543 38573', '+91 99999 45379']
        # contact_name_list = ['MALIK JOBS GROUP ||', 'infoITLeads #1','Indian Jobs']

        res = []
        for i in contact_name_list:
            if i not in res:
                if len(i) > 2:
                    res.append(i)
                else:
                    print(i)
        res.sort()
        print("total group found  =====>> ")
        print(res)
        print("all group found length =====>> " + str(len(res)))

        print("total group save in database =====>> ")
        total_save_group = 0
        total_save_group_aready_in_database = 0
        for single in res:
            try:
                # ct = datetime.datetime.now()
                group_name_class = Group_name_table(Group_name=single)
                records = self.session.query(Group_name_table).filter_by(Group_name=single).all()
                if len(records) == 0:

                    # if str(group_name_class.Group_name).startswith('+'):
                    #    group_name_class.Is_group_name_enable=False

                    self.session.add(group_name_class)
                    self.session.commit()

                    if str(group_name_class.Group_name.decode()).startswith('+'):
                        self.group_is_induvidual(group_name_class.id)

                    group_name_class.printclass()
                    # print(group_name_class)
                    # print(group_name_class.Group_name)
                    total_save_group = total_save_group + 1
                else:
                    total_save_group_aready_in_database = total_save_group_aready_in_database + 1
            except Exception as e:
                pass

        print("total new group save in database " + str(total_save_group))
        print("total_save_group_aready_in_database " + str(total_save_group_aready_in_database))

    def group_is_induvidual(self, group_id):
        try:
            self.session.query(Group_name_table).filter(Group_name_table.id == group_id).update(
                {'Is_group_name_enable': False})
            self.session.commit()
        except Exception as e:
            pass

    def check_mobile_is_connected_otr_not(self):

        from subprocess import PIPE, run

        command = ['adb', 'devices']
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        print(result.returncode, result.stdout, result.stderr)
        if deviceName in result.stdout:
            return True
        else:
            return False

        import subprocess
        com_str = subprocess.call("adb devices", shell=True)
        self.logger.info(com_str)
        self.logger.info("device is connected ..")

    def __init__(self):
        # self.logger = None
        self.session = None

        import logging

        self.logger = logging.getLogger(__name__)
        FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(asctime)s %(message)s"
        logging.basicConfig(format=FORMAT)

        # Create and configure logger
        # self.logging.basicConfig(filename="newfile.log", format='%(asctime)s %(message)s', filemode='w')

        # Creating an object
        self.logger = logging.getLogger()

        # Setting the threshold of logger to DEBUG
        self.logger.setLevel(logging.INFO)

    def clean_mobile_whatsapp_text_folder(self):
        try:
            print("remove all old csv files ")
            from subprocess import PIPE, run

            # delete .aaaa folder
            com = 'adb shell rm  -rR -v sdcard/.aaaa/'
            # command = ['adb', 'shell','rm','-rR','-v','sdcard/.aaaa/']
            command = ['adb', 'shell', 'rm', '-rR', 'sdcard/.aaaa/']
            result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            print(result.returncode, result.stdout, result.stderr)

            # create folder .aaaa
            com = 'adb shell mkdir   sdcard/.aaaa'
            command = ['adb', 'shell', 'mkdir', 'sdcard/.aaaa']
            result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            print(result.returncode, result.stdout, result.stderr)
        except Exception as e:
            self.logger.error(e)
            # pass

    def reluanch(self):
        start_time = time.time()
        print("programme start...")
        wh = Whatsapp_automate()
        wh.session = connect_to_database()

        connected = wh.check_mobile_is_connected_otr_not()
        if connected == False:
            wh.logger.info("please check your mobile connection")
            exit(0)

        wh.clean_mobile_whatsapp_text_folder()

        android = Myandroid()
        wh.driver = android.create_drive()
        android.go_to_home()
        android.open_whatsappp()

        wh.myscroll_bottom_to_top()

        wh.clean_filter_upload_in_db()

        print(wh.contact_name)
        print("--- %s seconds ---" % (time.time() - start_time))
        exit(0)


if __name__ == "__main__":
    for x in range(0, 2):
        start_time = time.time()
        print("programme start...")
        wh = Whatsapp_automate()
        wh.create_logging()
        # wh.session = connect_to_database()
        md = MondoBDConnection()
        group_name_collection = md.get_group_name_collection()
        group_txt_export_collection = md.get_group_txt_export_collection()
        wh.group_name_collection = group_name_collection
        wh.group_txt_export_collection = group_txt_export_collection
        connected = wh.check_mobile_is_connected_otr_not()
        if connected == False:
            wh.logger.info("please check your mobile connection")
            exit(0)

        wh.clean_mobile_whatsapp_text_folder()

        android = Myandroid()
        wh.driver = android.create_drive()
        android.go_to_home()
        android.open_whatsappp()

        wh.myscroll_bottom_to_top()

        wh.clean_filter_upload_in_db()

        print(wh.contact_name)
        print("--- %s seconds ---" % (time.time() - start_time))
    exit(0)

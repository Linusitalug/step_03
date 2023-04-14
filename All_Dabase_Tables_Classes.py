from sqlalchemy import create_engine, Column, Integer, String, \
    UnicodeText, DateTime, ForeignKey, Boolean, TEXT, LargeBinary, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from myconfiguration import db_password,db_name

Base=declarative_base()


engine = create_engine('mysql://root:'+db_password+'@localhost/'+db_name+'?charset=utf8mb4&use_unicode=0')

import datetime;
class Group_name_table(Base):
    __tablename__='group_name_table'
    id=Column(Integer,primary_key=True)
    Group_name=Column(Unicode(500), unique=True, nullable=False)
    Group_name_created_dataTime = Column(DateTime, nullable=False)
    Group_full_name = Column(UnicodeText(), nullable=False)
    Is_group_name_enable = Column(Boolean, unique=False)
    Group_type =Column(UnicodeText(), nullable=False)
    Allot_to=Column(UnicodeText(), nullable=True)


    group_txt_export = relationship("Group_Txt_Export")
    message = relationship("Message")

    def __init__(self,Group_name):
        self.Group_name = Group_name
        self.Group_full_name = ""
        self.Group_type = ""
        ct = datetime.datetime.now()
        self.Group_name_created_dataTime=ct
        self.Is_group_name_enable=True
        self.Allot_to="available"

    #def __str__(self):
    #    print("id "+str(self.id)+" group name"+str(self.Group_name)+" group created date "+str(self.Group_name_created_dataTime))

    def printclass(self):
        print("id " + str(self.id) + " group name  " + str(self.Group_name) + " group created date " + str(
            self.Group_name_created_dataTime))
    def __str__(self):
        return  ("id " + str(self.id) + " group name  " + str(self.Group_name.decode('unicode_escape')) + " group created date " + str(
            self.Group_name_created_dataTime))

class Group_Txt_Export(Base):
    __tablename__='group_txt_export'
    id=Column(Integer,primary_key=True)
    Group_name=Column(UnicodeText(), nullable=False,unique=False)
    Group_export_dataTime = Column(DateTime, nullable=False)
    Group_export_process_time = Column(Integer, nullable=False)
    Group_export_file_copy_system = Column(UnicodeText(), nullable=False)
    Group_export_file_name = Column(UnicodeText(), nullable=False)
    Group_export_file_convert_to_csv = Column(UnicodeText(), nullable=True)
    Group_export_file_csv_upload_in_db = Column(UnicodeText(), nullable=True)
    Group_export_data_file = Column(LargeBinary(length=(2**32)-1), nullable=True)
    Group_export_csv_file = Column(LargeBinary(length=(2**32)-1), nullable=True)
    Group_export_txt_file_size = Column(Integer, nullable=True)

    group_name_id = Column(Integer, ForeignKey('group_name_table.id'))

    def __init__(self,Group_name,Group_export_process_time,Group_export_file_name,
                 group_name_id,Group_export_data_file,Group_export_txt_file_size):
        ct = datetime.datetime.now()
        self.Group_export_dataTime=ct
        self.Group_name=Group_name
        self.Group_export_process_time=Group_export_process_time
        self.Group_export_file_copy_system='yes'
        self.Group_export_file_name=Group_export_file_name
        self.Group_export_file_convert_to_csv='no'
        self.Group_export_file_csv_upload_in_db='no'
        self.group_name_id=group_name_id
        self.Group_export_data_file=Group_export_data_file
        self.Group_export_txt_file_size=Group_export_txt_file_size


    def printclass(self):
        print("id " + str(self.id) + " group name  " + str(self.Group_name) + " group created date " + str(
            self.Group_export_dataTime))


class Message(Base):
    __tablename__='message'
    id=Column(Integer,primary_key=True)
    Date=Column(UnicodeText(), nullable=False)
    Time=Column(UnicodeText(), nullable=False)
    Author=Column(UnicodeText(), nullable=False,default='')
    Message=Column(UnicodeText(), nullable=False)
    DataTime = Column(DateTime, nullable=False)
    MyHashcode = Column(String(500), nullable=False,unique=False)
    MessageHashcode = Column(String(500), nullable=False, unique=True)

    group_name_id = Column(Integer, ForeignKey('group_name_table.id'))

    def __init__(self, Date, Time, Author, Message,DataTime,Group_name_id):
        self.Date=Date
        self.Time = Time
        self.Author = Author
        self.Message = Message
        self.DataTime = DataTime
        self.create_hash()
        self.group_name_id=Group_name_id


    def create_hash(self):
        import hashlib
        combine=self.Author+''+str(self.DataTime)+''+self.Message
        self.MyHashcode=hashlib.md5(combine.encode('utf-8')).hexdigest()
        combine_message = self.Message
        self.MessageHashcode = hashlib.md5(combine_message.encode('utf-8')).hexdigest()


def connect_to_database():
    #engine = create_engine('mysql://root:44bb6c3305bAa@localhost/whatsapp_data?charset=utf8mb4&use_unicode=0')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


if __name__ == "__main__":

    Base.metadata.create_all(engine) #Creates the table
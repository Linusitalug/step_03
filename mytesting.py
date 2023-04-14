from All_Dabase_Tables_Classes import connect_to_database, Group_name_table
from step_02_get_all_group_names_save_in_db_whatsapp_app__mobile import Whatsapp_automate

if __name__ == "__main__":

    print("programme start...")
    wh = Whatsapp_automate()
    wh.session = connect_to_database()
    all=wh.session.query(Group_name_table).all()


    group_name_class = wh.session.query(Group_name_table).filter_by(Group_name='🥸😍😘Sialkoty Boy😍😘🤣…').one()
    group_name='🥸😍😘Sialkoty Boy😍😘🤣…'
    group_name_class = wh.session.query(Group_name_table).filter_by(Group_name=group_name).one()
    wh.find_group_already_Today_scrap_or_not('🥸😍😘Sialkoty Boy😍😘🤣…')
    print()

class Constants:
    matches_front_old = r"Name([\w ]+)$|ID NO([\w ]+).|মাতা(.+)|Date of Birth(.+)|পিতা(.+)|নাম(.+)|স্বামী(.+)"
    matches_back_old = r"Blood Group(.+)|ঠিকানা(.+)|SST:(.+)"
    back_data = ['name', 'nid_no', 'mother_name', 'dob', 'father_name', 'bn_name', 'husband']
    front_data = ['blood_group', 'permanent_address', 'permanent_address']

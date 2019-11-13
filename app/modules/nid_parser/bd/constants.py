class Constants:
    matches_front_old = r"Name([\w ]+)|ID NO([\w ]+).|মাতা(.+)|Date of Birth(.+)|পিতা(.+)|নাম(.+)|স্বামী(.+)"
    matches_back_old = r"Blood Group(.+)|ঠিকানা(.+)|SST(.+)"
    front_data = ['name', 'nid_no', 'mother_name', 'dob', 'father_name', 'bn_name', 'husband', 'nid_no']
    back_data = ['blood_group', 'address', 'address']
    matches_front_new = r"(Name)|NID No(.+)|(মাতা)|Birth(.+)|(পিতা)|(নাম)|(স্বামী)|Nino(.+)?"

class Constants:
    matches_front_old = r"Name([\w ]+)$|ID NO([\w ]+).$|মাতা(.+)|Date of Birth(.+)|পিতা(.+)|নাম(.+)|স্বামী(.+)"
    matches_back_old = r"Blood Group(.+)|"
    back_data = ['name', 'nid_no', 'mother_name', 'dob', 'father_name', 'blood_group', 'bn_name', 'husband']

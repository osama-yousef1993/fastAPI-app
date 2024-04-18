def build_users_dict(row, type=""):
    data = dict()
    if type == "update":
        data["first_name"] = row[1]
        data["Last_name"] = row[2]
        data["email"] = row[3]
        data["profiles"] = row[5]
        data["otp"] = row[8]
        data["otp_expiration_time"] = row[9]
    else:
        data["first_name"] = row[0]
        data["Last_name"] = row[1]
        data["email"] = row[2]
        data["profiles"] = row[3]
        data["otp"] = row[4]
        data["otp_expiration_time"] = row[5]
    return data

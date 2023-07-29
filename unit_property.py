import json
import time
import pandas as pd

class unit_details:
    def __init__(self) -> None:
        self.data= self.property_data()
        self.people = self.data['people']
        self.devices=self.data['devices']
        self.address={"address":','.join(list(self.data['address'].values()))}
    def data_frame_in(self,data):
        """
        to print the details
        """
        df=pd.DataFrame(data)
        print(df)
    def moved_property_save(self,data):
        print("changed data saving to property_data_changes.json file")
        with open("property_data_changes.json", "w") as file:
            json_string = json.dumps(data,sort_keys=False, indent=2)
            file.write(json_string)
            
    def user_move(self,user):
        added_people=self.people.append(user)
        self.data['people']=added_people
        self.moved_property_save(self.data)
    def user_delete(self,first_name,last_name):
        rem_people=[x for x in self.people if x['first_name'] != first_name and x['last_name'] != last_name]
        self.data['people']=rem_people
        self.moved_property_save(self.data)
    def property_data(self):
        with open('property_data.json','r') as f:
            data =json.loads(f.read())
        return data
    
    def get_device(self,unit_devices,unit_no,roles):
        """
        To get device details using role and unit
        """
        device_details={}
        for key,device in unit_devices.items():
            device_p =[dev for dev in device for role in roles if dev['unit'] == int(unit_no) if (role == 'Resident' and dev['admin_accessible'] == 'false') or (role=='Admin' and dev['admin_accessible']=='true')]
            if len(device_p)!=0:
                device_details[key]=device_p
        return device_details
    def print_details(self,unit_det_with_res):
        print("listing user details:    ")
        self.data_frame_in(unit_det_with_res['user_details'])
        if 'admin_view_res' in unit_det_with_res.keys():
            print("listing all residents list which admin user can see")
            self.data_frame_in(unit_det_with_res['admin_view_res'])
        for device,value in unit_det_with_res['associate_devices'].items():
            print(f" unit no: {unit_no} with {device} device details")
            self.data_frame_in(value)
            
    def unit_no_res(self,unit_no):
        """
        retriving data based on unit_no
        """
        user = [x for x in self.people if x['unit']==unit_no and 'Resident' in x['roles']]
        if len(user)>0:
            unit_details =self.get_device(self.devices, unit_no, ['Resident'])
            unit_det_with_res={'user_details':user,'associate_devices': unit_details}
            self.print_details(unit_det_with_res)
        else:
            print(f"entered unit_no {unit_no} not in the unit list")
    def unit_user_res(self,first_name,last_name):
        """
        retriving data based on first_name & last_name
        """
        Admin=False
        user = [x for x in self.people if x['first_name'] == first_name and x['last_name'] == last_name]
        print(user)
        if len(user) == 0:
            print("Please Enter Valid User..")
        else:
            person_details = user[0]
            unit_details =self.get_device(self.devices, person_details['unit'],person_details['roles'])
            unit_det_with_res={'user_details':person_details,'associate_devices': unit_details}
            if 'Admin' in  person_details['roles']:
                rem_user=self.people
                unit_det_with_res['admin_view_res']=rem_user.remove(person_details)
                Admin=True
            self.print_details(unit_det_with_res) 
            return Admin    
        
if __name__=='__main__':
    print("unit object initializing")
    unit_object=unit_details()

    unit_no = input("Enter a  valid unit no: ")
    unit_object.unit_no_res(unit_no)
    print("                                                                       ")
    print("###################ENTER USER DETAILS##################################")
    print("                                                                        ")
    time.sleep(2)
    first_name=input("Enter First Name: ").capitalize()
    last_name=input("Enter Last Name: ").capitalize()
    user_detail= unit_object.unit_user_res(first_name,last_name)
    if user_detail:
        time.sleep(1)
        print("please choose one of the  opetion")
        print("1) please provide input as 1 for add new resident")
        print("2) please provide input as 2 for delete old resident")
        res_change=int(input("please Enter number 1 or 2 :"))
        chng_first_name=input("Enter First Name: ").capitalize()
        chng_last_name=input("Enter Last Name: ").capitalize()
        if res_change ==1:
            role=input("Enter Role: ").capitalize()
            unit_no =input("Enter unit number: ")
            new_user={"first_name":chng_first_name,"last_name":chng_last_name,"unit":unit_no,"roles":role}
            unit_object.user_move(new_user)
        elif res_change ==2:
            unit_object.user_delete(chng_last_name,chng_last_name)
        


        








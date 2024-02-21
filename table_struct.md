
Flow 
----------------------------------------------------------
|-> Login = {

}
|-> signup = {

}



Roles : Admin, members, 

Admin => Chapter creater
Members => Joiner

Chapter => {
    "Role" : []
}


------------------------------------------------------------
profile = {
    Display Name,
    Role, = > Important
    Bio,
    Chapters(Groups), => need to create separate Table
    Connections, => need to create  a new table for connections.
    gender,
    Birth Date,
    Address,
    Email,
    Industry,
    My Business = "Able to show the ckeditor details into profile",
}

---------------------------------------------------------

Connections_flow = {
    "profile llistout",
    "Add New Connections by searching in globally"
}
Connection_table = {
    "User_id" : "Connected User_id",
    "Status" : ["Pending","Accepted","Rejected"],
    
}


==============================================================

Profile = {
    Title:['Mr.','Mrs.','Miss','Ms.','Dr.'],
    First Name:"mandatory",
    Last Name:"mandatory",
    Suffix: "not mandatory",
    Display_Name:"not mandatory",
    Gender :[Male, Female],
    Company_Name: "not mandatory",
    Product/Service Description :"not mandatory",
    GST Registered State:"not mandatory",
    "IN (GST Identification Number). If no GSTIN, then only please provide PAN" : "not mandatory",
    Industry:"not mandatory",
    Classification:"not mandatory",
    Requested Speciality : "not mandatory",
    Membership_Status: [Active, Not Active],
    My Business: "show the ckeditor details here",
    Keywords (comma separated):  "not mandatory",

    # main Profle

    Username:"mandatory",
    Language: "mandatory",
    Timezone:"mandatory",
    Profile_Image:"not mandatory",
    Company_Logo: "not mandatory",

    # Contact Details
    Show me on BNI Public Websites: If checked the public will be able to search for your services,
    Billing Address Quick Copy : "not mandatory",
    Phone: "mandatory",
    Direct Number: "not mandatory",
    Home: "not mandatory",
    Mobile_Number : ,
    Pager: ,
    Voice Mail :,
    Toll Free,
    Fax:,
    Email  : "Need tyo verify",
    I would like to receive updates from BNI about its networking, events, promotions and special offers. : ,
    I would like to share my Revenue Received data with my BNI Director :,
    Website :,
    Social Networking Links: Multi Select [ Facebook, Twitter, LinkedIn, Google+, Skype, Yahoo!],

    # Address
    Which address should appear on your public profile?: [Main Address,  Billing,  None]
    Address Line 1: "mandatory",
    Address Line 2: "not mandatory",
    City:, 
    State:,
    Country:"mandatory",
    Zip/Postal Code:,

    # Billing
    Same as above: check box,
    Billing Address Line 1: "not mandatory",
    Billing Address Line 2: "not mandatory",
    Billing City:, 
    Billing State:,
    Billing Country:,
    Billing Zip/Postal Code:,



    Profile_Image:"not mandatory",
    Cover_Photo:"not mandatory",
    Phone_Number_1:"not mandatory",
    Phone_Number_2:"not mandatory",
    Skype_Id:"not mandatory",
    Facebook:"not mandatory",
    Twitter:"not mandatory",
    LinkedIn:"not mandatory",
    Address:  "Show Map",
    City:"not mandatory",
    Country:"not mandatory",
    Zipcode:"not mandatory",
    About Me :"not mandatory",
    Services Offering : "show services offered table",
    Availability :["Available for Hire","Not available for Hire"]


}

group = {
    Remaining groups you may create,
    Group Name,
    Access Type, 
    Group Type,
    Group Description, 
    Language,
    Invite Connections,
}
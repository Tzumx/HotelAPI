This project serves a simple hotel administrations system API that includes the following aspects (CRUD):

    * room categories can be created, viewed, updated, deleted and modified with features
    * rooms can be created, viewed, updated, and deleted
    * guests can be created, viewed, updated, and deleted
    * bookings can be created, viewed, updated, and deleted
    * payments can be created, viewed, updated, and deleted
    * requests can be created, viewed, updated, and deleted
    * users can be created, viewed, updated, and deleted by admins

## Room categories (types) 
Room categories have room's characteristics.<br>
[View rooms routers.](overview.md#rooms)

A room categories have basic information, such as:

    * id
    * name
    * price
    * description

## Room features
Room features have many-to-many connection with room categories. Each room can have some features and vice versa, each feature can be in many room's category.<br>
[View rooms routers.](overview.md#rooms)

A room features have basic information, such as:

    * id
    * feature

## Room
Room is the main unit when working with bookings. Each room must be connected with one room categories (types) to get information about price and features in the room.<br>
Rooms are identified by their room number.<br>
[View rooms routers.](overview.md#rooms)

A rooms have basic information, such as:

    * number
    * room category
    * number of the floor
    * number of the house

## Guests
[View guests routers.](overview.md#guests)<br>

Guests can have multiple bookings and have basic information, such as:

    * id
    * name
    * email
    * phone number

## Bookings
Bookings are connected to guests and rooms. When a guest makes a booking, only one room is assigned. Hotel staff can not change is_paid checkbox - it is calculated automatically based on payments.<br>
[View bookings routers.](overview.md#bookings)

Bookings have basic information, such as:

    * id
    * room number
    * guest id
    * check in date and time
    * check out date and time
    * description
    * is_paid (has the room been paid for)
    * is_active
    * client review
    * updated_at
    * created_at

## Payments
Payments have the information about all financial transactions. Each payment connected with one booking. After adding each payment is_paid checkbox is recalculating for connected booking.<br>
[View payments routers.](overview.md#payments)

Payments have basic information, such as:
    
    * id
    * booking id
    * sum of transaction
    * date of transaction
    * description

## Requests
For each booking can be created requests like "need to clean", "need to be repaired" etc.<br>
[View requests routers.](overview.md#requests)

Requests have basic information, such as:

    * id
    * booking id
    * description
    * is closed
    * close description
    * price
    * updated_at
    * created_at    

## Users
Have two types of users: ordinary staff and admins. Admins additionally can add, change and delete any user. First user will always be created as admin.<br>
[View users routers.](overview.md#users)


Users have basic information, such as:

    * id
    * email
    * name
    * password
    * is_active
    * is_admin
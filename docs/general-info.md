This project serves a simple hotel administrations system API that includes the following aspects (CRUD):

    * room categories can be created, viewed, updated, and deleted
    * rooms can be created, viewed, updated, and deleted
    * guests can be created, viewed, updated, and deleted
    * bookings can be created, viewed, updated, and deleted
    * payments can be created, viewed, updated, and deleted
    * requests can be created, viewed, updated, and deleted

## Room categories (types)
Room categories has room's characteristics.

A room category has basic information, such as:

    * id
    * name
    * price
    * description

## Room features
Room features has many-to-many connection with room categories. Each room can have some features and vice versa each feature can be in many room's category.

A room features has basic information, such as:

    * id
    * feature

## Room
Room is the main unit when working with bookings. Each room must be connected with one room categories (types) to get information about price and features in the room.
Rooms are identified by their room number.

A room has basic information, such as:

    * number
    * room category
    * number of the floor
    * number of the house

## Guests
Guests can have multiple bookings and have basic information, such as:

    * id
    * name
    * email
    * phone number

## Bookings
Bookings are connected to guests and rooms. When a guest makes a booking, only one room is assigned. Hotel staff can not change is_paid checkbox - it is calculated automatically based on payments.

Booking have basic information, such as:

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
Payments has the information about all financial transactions. Each payment connected with one booking. After adding each payment is_paid checkbox is recalculate for connected booking.

Payment have basic information, such as:
    
    * id
    * booking id
    * sum of transaction
    * date of transaction
    * description

## Requests
For each booking can be created requests like "need to clean", "need to be repaired" etc.

Requests have basic information, such as:

    * id
    * booking id
    * description
    * is closed
    * close description
    * price
    * updated_at
    * created_at    
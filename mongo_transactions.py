import pymongo
import pymongo.client_session

db_name = "users_information"
users_collection = "users"
contacts_collection = "contacts"


def prepare_database(mc: pymongo.MongoClient) -> None:
    mc.drop_database(db_name)

    db = mc.get_database(db_name)
    users = db.get_collection(users_collection)
    users.insert_many([
        {
            "nickname": "john_doe",
            "first_name": "John",
            "last_name": "Doe",
        },
        {
            "nickname": "jane_doe",
            "first_name": "Jane",
            "last_name": "Doe",
        },
    ])
    contacts = db.get_collection(contacts_collection)
    contacts.insert_many([
        {
            "nickname": "john_doe",
            "email": "john.doe@somemail.com",
        },
        {
            "nickname": "jane_doe",
            "email": "jane.doe@somemail.com",
        },
    ])


def update_users_information_tr(cs: pymongo.client_session.ClientSession) -> None:
    db = cs.client.get_database(db_name)
    users = db.get_collection(users_collection)
    users.update_one({"nickname": "john_doe"}, 
        {
            "$set": { "first_name": "Bob" }
        },
        session=cs,
    )
    contacts = db.get_collection(contacts_collection)
    contacts.update_one({"nickname": "john_doe"}, 
        {
            "$set": {"phone": "+1 (777) 333-22-11"}
        },
        session=cs,
    )
    contacts.update_one({"nickname": "john_doe"},
        {
            "$unset": {"email": ""}
        },
        session=cs,
    )


def main() -> None:
    uri = "mongodb://127.0.0.1:27017/?replicaSet=rs0&directConnection=true"
    with pymongo.MongoClient(uri) as mc:
        prepare_database(mc)
        with mc.start_session() as cs:
            cs.with_transaction(callback=update_users_information_tr)


if __name__ == "__main__":
    main()

db.createUser(
    {
        user: "yakubov",
        pwd: "password",
        roles: [
            {
                role: "readWrite",
                db: "info_bot_db"
            },
            {
                role: "readWrite",
                db: "aiogram_fsm"
            },
        ]
    }
)
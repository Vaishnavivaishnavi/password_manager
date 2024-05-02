This project makes end-user life simple by auto-filling credentials (username, password) for website login for user, user just need to authenticate with his master password, rest is done by Password Manager. 

When first time user request to store a password, it encrypts user and password using AES 256 Bit and stores the data in DB. Whenever password login requested user has to authenticate with master password and specific website password will be auto filled if it is stored in DB.

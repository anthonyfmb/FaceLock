## What it does
When creating a new account for a website, this project will analyze your face and create and store a password in a Django database. Then, if you wish to sign back into the website, the program will analyze your face, match it with the existing face, and autofill the password section with your password.
## How we built it
Python was the foundation of the project and used exclusively for the GUI and autofilling the password on an existing web browser. Opencv was used to capture the face of the user. Tensorflow was used to create a four layer neural network with binary classification. Django was used for a database.

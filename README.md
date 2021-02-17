# ZID ARTCC Website Code
*These instructions are based on Unix/Linux systems (including MacOS). Certain commands will need to be altered (especially file paths) if running on Windows.*

## Prerequisites
To run the development server, you must have the following installed:
- Python (version 3.7 or higher)
- Pip
- Venv (optional; recommended)

## PostgreSQL
To run the development server locally, you will need to set up a local PostgreSQL instance. [This article](https://www.prisma.io/dataguide/postgresql/setting-up-a-local-postgresql-database) is a good starting point for setup on Windows, MacOS, and Linux.

To access the AWS parameters that include the database credentials, you will need to contact the ZID Webmaster to be set up with an AWS account. You will not be able to run the code locally without this access.

## Setup
If you are running the development server in a virtual environment, run the following commands in a terminal window to initialize and activate your environment:

`python3 -m venv env`

`source env/bin/activate`

Next, install the required Python libraries:

`python3 -m pip install -r requirements.txt`

Before running your development server, you will need to initialize your environment variables. Make a copy of the `.env.example` file and rename it to `.env`. **DO NOT COMMIT THIS FILE TO SOURCE CONTROL!** Edit the values in `.env` to match your ARTCC configuration.

Once the `.env` file is setup, you will need to migrate to your local database. Run the following commands:

`python3 manage.py makemigrations`

`python3 manage.py migrate`

## Running the Development Server

Once all setup steps are complete, run your Django development server by running:

`python3 manage.py runserver [PORT]`

where `[PORT]` is an optional argument specifying the local port to run the server on. If you do not include this, Django defaults to port 8000. You can now access the development server by going to `http://localhost:[PORT]` in your browser.

To use/test ULS authentication with VATUSA, you must configure the redirect URLs on the VATUSA facility management page. Go to `templates/partials/navbar.html` and change the URL number in the VATUSA login link to correspond with the correct URL on VATUSA.

## Development Flow

The `master` branch is configured to not allow push actions. Feature, bugfix, and refactor branches should be made from the `dev` branch. Once work is complete, open a pull request from your working branch into `dev`. Pull requests to `master` require one approving review.

## Credits
Much of the backend/database logic is based on Michael Romashov's website for the ZHU artcc. His wonderful work can be found [here](https://github.com/MikeRomaa/zhuartcc.org).
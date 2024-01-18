# *** SCHOOL PROJECT ***


# Gatekeeper-Back-end
Backend for the Gatekeeper app


Event Planning Webapp.

Welcome to the event planning webapp! This app allows you to easily create and manage event pages, invite guests, and check in attendees using QR code scanning technology.

Getting Started.

To get started with the app, you'll need to sign up for an account. Once you're logged in, you can create an event page, add details about the event, and invite guests. You can also use the QR code scanning feature to check in attendees and keep track of who has arrived.

Features.

Create and manage event pages
Invite guests and keep track of RSVPs
Use QR code scanning to check in attendees
Customize event pages with all the details your guests need to know

## Local Setup Guide

### Prerequisites
- Python (3.11 or suitable version)
- PostgreSQL
- PostGIS
- GDAL

### Installation Instructions

#### Install PostgreSQL and PostGIS
On Debian-based systems:
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo apt-get install postgis postgresql-12-postgis-3


#### Install GDAL
For Debian-based systems:
sudo apt-get install libgdal-dev


#### Install project
pip install -r requirements/local.txt
Create a .env file in the root directory of the project and add the following variables:
DATABASE_URL=postgis://username:password@localhost:5432/databasename

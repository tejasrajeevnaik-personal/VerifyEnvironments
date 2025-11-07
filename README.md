Overview:\
This project automates the verification of login functionality across four environments: dev, dev-int, test, and staging.
Each environment is validated against five types of logins:
1. UI SSO Login
2. UI User Login with OTP verification
3. Server SFTP (Password-based) Login
4. Server SFTP (SSH Key-based) Login
5. Server FTPS Login

Purpose:\
The goal of this project is to eliminate repetitive manual checks and ensure that environment supporting services remain healthy and functional at all times.

Key Features:\
✅ Automated execution via a single double-clickable .bat file\
✅ Automatic OTP retrieval from Gmail (for login verification)\
✅ Automatic email reporting sent to stakeholders after execution\
✅ Acts as a daily environment hygiene checker to catch issues early

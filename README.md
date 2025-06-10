# Automation for SRH

If you don't know what SRH is, consider yourself lucky.


## Setup

1. Install docker <https://docs.docker.com/get-started/get-docker/>

2. Create a `env` file:
```env
LOGIN_URL=URL-of-the-SRH-login-page
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
USERNAME=yourUsername
PASSWORD=yourPassword
```

3. Build the image
```bash
./build.sh
```

4. Run the image to get a shell
```bash
./run-stable.sh
```

5. Then in the image shell:
```bash
./register.py today office
```
```bash
./register.py yesterday remote
```
```bash
./register.py '2 days ago' office
```
and so on.

Video captures are stored in `./videos/`.

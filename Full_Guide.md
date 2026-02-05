# 📧 SMTP Mail Server Setup Lab - Fresh Installation Guide

## Complete Step-by-Step with Screenshot & Explanation Requirements

> **PURPOSE:** This guide is designed for you to follow while setting up a FRESH Rocky Linux mail server and Ubuntu client. Take a screenshot after EVERY command and document what each command does.

---

## 🎯 Lab Requirements

### What You Need

- ✅ Fresh Rocky Linux VM (for mail server)
- ✅ Fresh Ubuntu VM (for mail client)
- ✅ VirtualBox NAT Network configured
- ✅ Screenshot tool ready (Snipping Tool, ShareX, etc.)
- ✅ This guide open on your host machine

### IP Configuration

- **Rocky Linux (Server):** 192.168.200.3
- **Ubuntu (Client):** 192.168.200.80
- **Gateway:** 192.168.200.2
- **Domain:** bungkus.org
- **FQDN:** bnaserver.bungkus.org

### User Account

- **Username:** dineesh
- **Password:** Lab2026

---

## 📋 Documentation Requirements

For **EVERY COMMAND** you must:

1. ✅ Take a screenshot showing the command AND its output
2. ✅ Write a brief explanation of what the command does
3. ✅ Note any important output or results

**Example Format:**

```
Command: sudo hostnamectl set-hostname bnaserver.bungkus.org

Explanation: This command sets the fully qualified domain name (FQDN) for the 
mail server. The FQDN is required for proper mail server identification and 
SSL certificate generation.

[SCREENSHOT: Shows the command being executed in terminal]

Expected Output: No output means success. The hostname is changed immediately.
```

---

# PART 1: ROCKY LINUX SERVER SETUP

## Phase 1: Initial System Configuration

### Step 1: Create User Account

**Command:**

```bash
sudo adduser dineesh
```

**Explanation:** Creates a new system user account named "dineesh" that will be used for email authentication. Mail servers use Linux system accounts for user authentication.

<img width="1320" height="213" alt="Screenshot 2026-02-05 090259" src="https://github.com/user-attachments/assets/384e72c5-a5a1-42f0-9115-d06b14108052" />

**What to document:**

- The command entered
- Password prompts appearing
- Full name and user info prompts

---

**Command:**

```bash
sudo passwd dineesh
```

**Explanation:** Sets the password "Lab2026" for the dineesh user account. This password will be used later for SMTP/IMAP authentication when connecting with email clients.

<img width="1569" height="384" alt="Screenshot 2026-02-05 091115" src="https://github.com/user-attachments/assets/b71a21fe-df88-4cf3-8120-29f38dea7112" />

**What to document:**

- Password prompt
- Success confirmation message

---

### Step 2: Set Hostname

**Command:**

```bash
sudo hostnamectl set-hostname bnaserver.bungkus.org
```

**Explanation:** Sets the Fully Qualified Domain Name (FQDN) of the server. This is critical because:

- Mail servers identify themselves using FQDN
- SSL certificates are issued to the FQDN
- Other mail servers use this for routing

<img width="2074" height="184" alt="Screenshot 2026-02-05 091311" src="https://github.com/user-attachments/assets/555efc67-d7bd-4c9e-9fdc-82847b697bbb" />

---

**Command:**

```bash
hostnamectl
```

**Explanation:** Verifies the hostname was set correctly. This displays system information including the static hostname, which should now be "bnaserver.bungkus.org".

<img width="1523" height="809" alt="Screenshot 2026-02-05 091411" src="https://github.com/user-attachments/assets/47f329a0-9e59-4baf-8e76-5ab1e5d90385" />

**What to document:**

- Static hostname field showing bnaserver.bungkus.org
- Operating system information
- Kernel version

---

**Command:**

```bash
hostname -f
```

**Explanation:** Displays only the FQDN (Fully Qualified Domain Name). This is a quick way to verify the hostname is correct before proceeding.

<img width="948" height="192" alt="Screenshot 2026-02-05 091438" src="https://github.com/user-attachments/assets/72db8e84-30b5-466c-b4e3-8d424b7dbd01" />

**Expected Output:** `bnaserver.bungkus.org`

---

### Step 3: Configure Hosts File

**Command:**

```bash
sudo nano /etc/hosts
```

**Explanation:** Opens the hosts file for editing. This file maps IP addresses to hostnames locally, allowing the server to resolve its own hostname without DNS.

<img width="1242" height="146" alt="Screenshot 2026-02-05 091525" src="https://github.com/user-attachments/assets/9a1a0a64-72bb-47e0-b4c0-b089c22e88a0" />

<img width="2531" height="1529" alt="Screenshot 2026-02-05 091601" src="https://github.com/user-attachments/assets/f84f8b68-c2a4-4b2e-a9d3-cce78f9c3651" />


---

**What to Add:**

```
192.168.200.3 bnaserver.bungkus.org bnaserver
```

**Explanation:** This entry tells the server:

- "When you see bnaserver.bungkus.org or bnaserver, use IP 192.168.200.3"
- This is essential for the mail server to identify itself correctly
- Without this, services may fail to start or malfunction

<img width="2226" height="277" alt="Screenshot 2026-02-05 091648" src="https://github.com/user-attachments/assets/839505f1-3441-4693-9332-c8b76dddce1a" />

**What to document:**

- The complete /etc/hosts file with your addition
- Highlight the line you added

---

**Command to Save:**

- Press `Ctrl + O` (WriteOut)
- Press `Enter` (Confirm filename)
- Press `Ctrl + X` (Exit)

<img width="2359" height="261" alt="Screenshot 2026-02-05 091753" src="https://github.com/user-attachments/assets/ffaa4f5a-77d8-4ba1-995f-de4af5ec2f8e" />

---

**Command:**

```bash
cat /etc/hosts
```

**Explanation:** Displays the contents of the hosts file to verify your changes were saved correctly.

<img width="2230" height="295" alt="Screenshot 2026-02-05 091824" src="https://github.com/user-attachments/assets/8533d07e-0415-49c0-856f-61e9c0f3ee6e" />

**What to document:**

- Verify the line you added is present
- Show localhost and other default entries

---

### Step 4: Network Verification

**Command:**

```bash
ip addr show
```

**Explanation:** Displays all network interfaces and their IP addresses. Use this to verify your server has the correct IP (192.168.200.3) assigned.

<img width="2535" height="819" alt="Screenshot 2026-02-05 092005" src="https://github.com/user-attachments/assets/6e3beb8e-8abb-4896-904c-dc7505d93abb" />

**What to document:**

- Interface name (usually enp0s3 or similar)
- IP address 192.168.200.3
- Netmask and broadcast address

---

**Command:**

```bash
ip route
```

**Explanation:** Shows the routing table, including the default gateway. This is critical - we learned that hostname changes can sometimes remove the gateway!

<img width="2288" height="264" alt="Screenshot 2026-02-05 092024" src="https://github.com/user-attachments/assets/99c5b36e-b837-4b08-aebc-c4ad0542e444" />

**What to document:**

- Default route (check if you have "default via 192.168.200.X" - could be .1 or .2)
- Local network route (192.168.200.0/24)

**🚨 IMPORTANT:** If you don't see ANY "default via" line, you need to add one!

---

**Command (ONLY if NO default gateway exists):**

```bash
sudo ip route add default via 192.168.200.1 dev enp0s3
```

**Explanation:** Manually adds the default gateway to the routing table. Replace "enp0s3" with your actual interface name from `ip addr show`.

**Note:** Most VirtualBox NAT networks use 192.168.200.1 as the gateway. If you already had a gateway (like .2), keep whatever you have - don't delete it! Only run this command if the gateway was completely missing.

<img width="2216" height="150" alt="image" src="https://github.com/user-attachments/assets/1e953ed2-3539-4ebe-be22-629dccde2c2a" />

**What to document:**

- Whether you had to add the gateway or it was already there
- Which gateway IP is being used (.1 or .2)
- Confirmation internet will work with this gateway

---

**Command:**

```bash
ping -c 3 8.8.8.8
```

**Explanation:** Tests internet connectivity by pinging Google's DNS server. Sends 3 ICMP packets and waits for replies.

<img width="1862" height="482" alt="image" src="https://github.com/user-attachments/assets/24aa5ce0-8df1-49cf-8ea2-2c8b7bd61c34" />

**What to document:**

- Whether packets are received (success) or lost (failure)
- Round-trip time

**⚠️ IMPORTANT - VirtualBox NAT Limitation:**

**If ping fails with "Network unreachable" or 100% packet loss, this is NORMAL!**

VirtualBox NAT networks block ICMP (ping) packets for security reasons, even when internet connectivity is fully functional. This does NOT indicate a problem with your mail server setup.

**For your documentation, explain:**

- Ping failed due to VirtualBox NAT blocking ICMP traffic
- This is expected behavior in NAT network mode
- Not an error - internet connectivity is verified using curl instead (next step)

---

**Command:**

```bash
curl -I https://google.com
```

**Explanation:** Tests HTTP/HTTPS connectivity by fetching headers from Google. This is a more reliable internet test than ping in VirtualBox environments.

<img width="2537" height="962" alt="image" src="https://github.com/user-attachments/assets/4e1133e9-ae51-4446-bbe1-ebbb00ac01bb" />

**What to document:**

- HTTP status code (should be 301 or 302)
- Headers received
- Confirms internet is working

---

### Step 5: Install Required Packages

**Command:**

```bash
sudo dnf update -y
```

**Explanation:** Updates all currently installed packages to their latest versions. The `-y` flag automatically answers "yes" to all prompts. This ensures you have the latest security patches before installing new software.

<img width="1228" height="141" alt="image" src="https://github.com/user-attachments/assets/2a8f8d8e-edb6-4eeb-baf6-3fb0dbb7d2c6" />

<img width="1629" height="1525" alt="image" src="https://github.com/user-attachments/assets/a104f412-28ff-4f0f-b09c-47ceedd0f479" />


**What to document:**

- Number of packages being updated
- Download size
- Completion message

---

**Command:**

```bash
sudo dnf install postfix dovecot -y
```

**Explanation:** Installs two essential mail server packages:

- **Postfix**: Mail Transfer Agent (MTA) - handles SMTP (sending/receiving email)
- **Dovecot**: IMAP/POP3 Server - allows mail clients to retrieve email

<img width="1178" height="78" alt="image" src="https://github.com/user-attachments/assets/90f9cce7-ce3a-4178-b3da-1954ab372e5a" />

<img width="2538" height="1494" alt="image" src="https://github.com/user-attachments/assets/52e82512-7dd5-4b52-b4c9-791dc0e029bb" />


**What to document:**

- Package names being installed
- Dependencies being added
- Total download size
- "Complete!" message

---

**Command:**

```bash
rpm -qa | grep postfix
```

**Explanation:** Verifies Postfix was installed successfully by querying the RPM package database and filtering for postfix-related packages.

<img width="1277" height="238" alt="image" src="https://github.com/user-attachments/assets/c68570a5-3b9b-4977-b4c2-7654ac2dc420" />

**Expected Output:** `postfix-3.x.x-x.el9.x86_64` (version numbers may vary)

---

**Command:**

```bash
rpm -qa | grep dovecot
```

**Explanation:** Verifies Dovecot installation the same way as above.

<img width="1219" height="252" alt="image" src="https://github.com/user-attachments/assets/8fe362b6-1953-46b4-b313-b3470840436c" />

**Expected Output:** Multiple dovecot packages (dovecot, dovecot-core, etc.)

---

## Phase 2: SSL/TLS Certificate Generation

### Step 6: Generate Self-Signed Certificate

**Command:**

```bash
sudo openssl req -new -x509 -days 365 -nodes \
  -out /etc/pki/tls/certs/bnaserver.pem \
  -keyout /etc/pki/tls/private/bnaserver.key \
  -subj "/C=MY/ST=KL/L=APU/O=SNA/CN=bnaserver.bungkus.org"
```

**Explanation:** Generates a self-signed SSL/TLS certificate that lasts 365 days. Let's break down each part:

- `openssl req`: Request certificate generation
- `-new -x509`: Create a new self-signed X.509 certificate
- `-days 365`: Certificate valid for 1 year
- `-nodes`: No passphrase (so services can auto-start)
- `-out`: Where to save the certificate file
- `-keyout`: Where to save the private key
- `-subj`: Certificate details (Country, State, Location, Organization, Common Name)
- **CN=bnaserver.bungkus.org**: MUST match your hostname!

<img width="2549" height="1005" alt="image" src="https://github.com/user-attachments/assets/9a3c1a22-c5fc-41e6-9b8b-6fa46f08fd17" />

**Expected Output:** Usually no output means success

---

**Command:**

```bash
sudo ls -l /etc/pki/tls/certs/bnaserver.pem
```

**Explanation:** Verifies the certificate file was created and shows its permissions and size.

<img width="2151" height="221" alt="image" src="https://github.com/user-attachments/assets/939e5428-cfc4-41d4-b416-6195794bd76f" />

**What to document:**

- File size (should be around 1-2 KB)
- Permissions
- Creation timestamp

---

**Command:**

```bash
sudo ls -l /etc/pki/tls/private/bnaserver.key
```

**Explanation:** Verifies the private key was created. This file is extremely sensitive!

<img width="2197" height="233" alt="image" src="https://github.com/user-attachments/assets/c80f46f5-b5b2-42c4-bd75-c347fac25ea2" />

**What to document:**

- File permissions (should be restrictive)
- File size

---

### Step 7: Set Proper Certificate Permissions

**Command:**

```bash
sudo chmod 600 /etc/pki/tls/private/bnaserver.key
```

**Explanation:** Sets permissions to 600 (read/write for owner only) on the private key. This is critical for security:

- 6 (owner): read + write
- 0 (group): no access
- 0 (others): no access
Only root can read/write this file, preventing unauthorized access to your encryption key.

<img width="2022" height="153" alt="image" src="https://github.com/user-attachments/assets/2d307ef2-ee57-4948-8d8a-ba706d7ede6c" />

---

**Command:**

```bash
sudo chmod 644 /etc/pki/tls/certs/bnaserver.pem
```

**Explanation:** Sets permissions to 644 on the certificate (public key). This allows:

- 6 (owner): read + write
- 4 (group): read only
- 4 (others): read only
The certificate can be publicly readable since it's meant to be shared with clients.

<img width="1979" height="181" alt="image" src="https://github.com/user-attachments/assets/ebdd51e8-4058-40b6-8d02-644911eb3f50" />

---

**Command:**

```bash
sudo openssl x509 -in /etc/pki/tls/certs/bnaserver.pem -text -noout
```

**Explanation:** Displays the certificate details in human-readable format without showing the encoded certificate data. Use this to verify:

- The Common Name (CN) matches your hostname
- Validity dates
- Signature algorithm

<img width="2114" height="63" alt="image" src="https://github.com/user-attachments/assets/18269c2f-8ed9-41d7-b0e3-abd2d3983913" />

<img width="1063" height="1352" alt="image" src="https://github.com/user-attachments/assets/73b35baa-b961-49e0-9f2c-3cbc19ea5a53" />

**What to document:**

- Subject line showing CN=bnaserver.bungkus.org
- Validity dates (Not Before / Not After)
- Issuer (should be same as Subject for self-signed)

---

## Phase 3: Postfix Configuration

### Step 8: Backup Original Configuration

**Command:**

```bash
sudo cp /etc/postfix/main.cf /etc/postfix/main.cf.backup
```

**Explanation:** Creates a backup of the original Postfix configuration file before making changes. This allows you to restore defaults if something goes wrong.

<img width="2173" height="174" alt="image" src="https://github.com/user-attachments/assets/1e6e8fb5-42d9-4114-b741-dd34f94395e4" />

---

**Command:**

```bash
ls -l /etc/postfix/main.cf*
```

**Explanation:** Lists both the original and backup configuration files to verify the backup was created.

<img width="2012" height="351" alt="image" src="https://github.com/user-attachments/assets/bc5f6f55-c48f-47ad-a1c8-2b9124c77d1a" />

---

### Step 9: Edit Postfix Main Configuration

**Command:**

```bash
sudo nano /etc/postfix/main.cf
```

**Explanation:** Opens the main Postfix configuration file for editing. This file controls all SMTP server behavior.

<img width="1468" height="109" alt="image" src="https://github.com/user-attachments/assets/408fa42a-38e5-45c6-9ce0-bb9a892bc7e8" />

---

**Configuration to Add/Modify:**

Find or add these lines (use Ctrl+W to search in nano):

```bash
# Basic Settings
myhostname = bnaserver.bungkus.org
mydomain = bungkus.org
myorigin = $mydomain
inet_interfaces = all
mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain
home_mailbox = Maildir/

# Network Settings
mynetworks = 192.168.200.0/24, 127.0.0.0/8

# TLS/SSL Settings
smtpd_tls_cert_file = /etc/pki/tls/certs/bnaserver.pem
smtpd_tls_key_file = /etc/pki/tls/private/bnaserver.key
smtpd_tls_security_level = may
smtpd_tls_auth_only = yes
smtpd_tls_loglevel = 1

# SASL Authentication
smtpd_sasl_type = dovecot
smtpd_sasl_path = private/auth
smtpd_sasl_auth_enable = yes
smtpd_sasl_security_options = noanonymous
smtpd_sasl_local_domain = $myhostname
broken_sasl_auth_clients = yes


# Mailbox Format
home_mailbox = Maildir/

```

**Explanation of Each Section:**

**Basic Settings:**

- `myhostname`: Server's FQDN - identifies the server in SMTP conversations
- `mydomain`: Base domain name
- `myorigin`: Domain to append to mail from local users
- `inet_interfaces`: Which network interfaces to listen on (all = all interfaces)
- `mydestination`: Domains this server accepts mail for (as final destination)

**Network Settings:**

- `mynetworks`: Trusted networks that can relay mail (your local network + localhost)

**TLS/SSL Settings:**

- `smtpd_tls_cert_file`: Path to your SSL certificate (public key)
- `smtpd_tls_key_file`: Path to your private key
- `smtpd_tls_security_level = may`: Offer STARTTLS but don't require it (for port 25)
- `smtpd_tls_auth_only = yes`: Only allow authentication over encrypted connections
- `smtpd_tls_loglevel`: How much TLS info to log (1 = basic)

**SASL Authentication:**

- `smtpd_sasl_type = dovecot`: Use Dovecot for authentication
- `smtpd_sasl_path`: Socket path where Dovecot auth is listening
- `smtpd_sasl_auth_enable`: Enable SASL authentication
- `smtpd_sasl_security_options`: Disable anonymous authentication
- `broken_sasl_auth_clients`: Support for older mail clients


<img width="1918" height="502" alt="image" src="https://github.com/user-attachments/assets/401ac7fe-11ec-4ef3-81d6-ef4a18e0672d" />

<img width="634" height="95" alt="image" src="https://github.com/user-attachments/assets/5818ad15-fae4-48c7-93cf-c8413947261f" />

<img width="668" height="123" alt="image" src="https://github.com/user-attachments/assets/f197d458-7499-4c70-ae30-bf0c621b4aeb" />

<img width="2040" height="241" alt="image" src="https://github.com/user-attachments/assets/a2938f7a-5519-428a-ae64-5f5798c5f2df" />

<img width="1278" height="94" alt="image" src="https://github.com/user-attachments/assets/f04e2711-ee3d-48ab-adc5-0b575d30f5f9" />

<img width="1791" height="427" alt="image" src="https://github.com/user-attachments/assets/7367692e-2960-444c-8928-27797386931d" />

<img width="865" height="127" alt="image" src="https://github.com/user-attachments/assets/d6c4408d-056e-4499-a1a7-895852f953be" />

<img width="1176" height="355" alt="image" src="https://github.com/user-attachments/assets/aacf0735-c688-41ff-8ac2-91c894df3a57" />

<img width="779" height="155" alt="image" src="https://github.com/user-attachments/assets/ded09ec8-4802-4de9-b94f-88f8f8581bc0" />





**What to document:**

- Scroll through and capture all the sections you modified
- Highlight the key changes

---

**Save and Exit:**

- Ctrl+O (save)
- Enter (confirm)
- Ctrl+X (exit)

<img width="1769" height="260" alt="image" src="https://github.com/user-attachments/assets/97ebd9d8-bb65-4a96-af22-bd6ceedfa433" />

---

**Command:**

```bash
sudo postconf -n
```

**Explanation:** Displays only the non-default settings in Postfix configuration (excludes all the commented default values). This makes it easy to see what you've actually changed.

<img width="2121" height="1414" alt="image" src="https://github.com/user-attachments/assets/2142ce9c-b78d-4628-b88c-057dadf11de0" />

**What to document:**

- All the settings you just configured
- Verify no syntax errors

---

### Step 10: Configure Postfix Master (Ports Configuration)

**Command:**

```bash
sudo cp /etc/postfix/master.cf /etc/postfix/master.cf.backup
```

**Explanation:** Backup master.cf before editing (same as we did with main.cf)

<img width="2272" height="191" alt="image" src="https://github.com/user-attachments/assets/03738ed1-6ed2-4d0e-8abb-1cb3dc33a5cc" />

---

**Command:**

```bash
sudo nano /etc/postfix/master.cf
```

**Explanation:** Opens the Postfix master configuration file which controls which services run on which ports.

<img width="1644" height="159" alt="image" src="https://github.com/user-attachments/assets/41213e15-4013-4fef-804c-8ac15e5930ce" />


---

**Find and Uncomment/Edit These Sections:**

**For Port 587 (Submission - STARTTLS):**

```
submission inet n       -       n       -       -       smtpd
  -o syslog_name=postfix/submission
  -o smtpd_tls_security_level=encrypt
  -o smtpd_sasl_auth_enable=yes
  -o smtpd_sasl_type=dovecot
  -o smtpd_sasl_path=private/auth
  -o smtpd_client_restrictions=permit_sasl_authenticated,reject
```

**Explanation:**

- `submission inet`: Defines service on port 587
- `smtpd_tls_security_level=encrypt`: REQUIRE encryption (STARTTLS mandatory)
- `smtpd_sasl_auth_enable=yes`: Require authentication
- Client must auth before sending mail

<img width="2232" height="722" alt="image" src="https://github.com/user-attachments/assets/40a04588-1bf6-4a7d-aa1a-91e8158a1299" />

---

**For Port 465 (SMTPS - TLS Wrapper):**

```
smtps     inet  n       -       n       -       -       smtpd
  -o syslog_name=postfix/smtps
  -o smtpd_tls_wrappermode=yes
  -o smtpd_sasl_auth_enable=yes
  -o smtpd_sasl_type=dovecot
  -o smtpd_sasl_path=private/auth
  -o smtpd_client_restrictions=permit_sasl_authenticated,reject
```

**Explanation:**

- `smtps inet`: Defines service on port 465
- `smtpd_tls_wrappermode=yes`: Immediate TLS (no STARTTLS, encrypted from start)
- Also requires authentication before sending

<img width="1867" height="695" alt="image" src="https://github.com/user-attachments/assets/27a02d9b-7134-44df-87eb-8805add01c3c" />

---

**Save and Exit nano**

<img width="2324" height="379" alt="image" src="https://github.com/user-attachments/assets/543aac53-f963-4b36-ae6c-fb5893dc91df" />

---

## Phase 4: Dovecot Configuration
### Step 11: Configure Dovecot Mail Location

**Command:**

```bash
sudo nano /etc/dovecot/conf.d/10-mail.conf
```

**Explanation:** Tells Dovecot where to find user emails. By default, it might be looking in the wrong place. We need to match the "Maildir" setting we just configured in Postfix.

<img width="1810" height="86" alt="image" src="https://github.com/user-attachments/assets/d22beab2-8356-45a0-87e2-879e210203c2" />

---

**Find and Modify:**

Find the line starting with `mail_location =` and change it to:

```
mail_location = maildir:~/Maildir
```

**Explanation:**

- `maildir:`: Use the Maildir format (one file per email)
- `~/Maildir`: Store emails in the "Maildir" folder inside each user's home directory (e.g., `/home/dineesh/Maildir`)

<img width="1057" height="244" alt="image" src="https://github.com/user-attachments/assets/cde6c42b-cbc8-4777-956f-67490ce2ea26" />

---

**Save and exit**

<img width="1817" height="393" alt="image" src="https://github.com/user-attachments/assets/b9e84005-ba3a-49c3-9f19-45343130f238" />

---

### Step 12: Configure Dovecot SSL

**Command:**

```bash
sudo nano /etc/dovecot/conf.d/10-ssl.conf
```

**Explanation:** Opens Dovecot's SSL configuration file where we specify certificate paths and SSL requirements.

<img width="1869" height="122" alt="image" src="https://github.com/user-attachments/assets/27fb6a4d-f260-4c36-b345-938ac3448b8b" />

---

**Command:**

```bash
sudo nano /etc/dovecot/conf.d/10-mail.conf
```

**Explanation:** Opens Dovecot's SSL configuration file where we specify certificate paths and SSL requirements.

<img width="1773" height="147" alt="image" src="https://github.com/user-attachments/assets/b9e6115b-64b1-411a-bf8d-fa8a32c3a433" />

---


**Find and Modify:**

```
ssl = required
ssl_cert = </etc/pki/tls/certs/bnaserver.pem
ssl_key = </etc/pki/tls/private/bnaserver.key
ssl_min_protocol = TLSv1.2
```

**Explanation:**

- `ssl = required`: Force SSL/TLS for all connections
- `ssl_cert = <`: The `<` means "read content from this file"
- Paths to our certificate and private key
- `ssl_min_protocol`: Don't allow old insecure TLS versions

<img width="2293" height="510" alt="image" src="https://github.com/user-attachments/assets/d8b3e924-35ee-499d-afe4-398182dc978e" />

---

**Save and exit**

<img width="2326" height="239" alt="image" src="https://github.com/user-attachments/assets/afdc8b09-9757-4597-92f0-92ba523ede96" />

---

### Step 13: Configure Dovecot Authentication

**Command:**

```bash
sudo nano /etc/dovecot/conf.d/10-auth.conf
```

**Explanation:** Configures how Dovecot authenticates users (using system accounts).

<img width="1836" height="150" alt="image" src="https://github.com/user-attachments/assets/bb081858-c49e-40f7-a42a-13325e0246c2" />

<img width="2559" height="1572" alt="image" src="https://github.com/user-attachments/assets/30bfec94-e90a-40af-b5a5-9f789b63797d" />


---

**Find and verify/modify:**

```
disable_plaintext_auth = yes
auth_mechanisms = plain login
```

**Explanation:**

- `disable_plaintext_auth = yes`: Don't allow passwords over unencrypted connections
- `auth_mechanisms = plain login`: Allow PLAIN and LOGIN auth methods (over TLS)

<img width="2049" height="320" alt="image" src="https://github.com/user-attachments/assets/fd2e5587-79de-45ef-b7cb-b7bf1904f16a" />

<img width="2173" height="342" alt="image" src="https://github.com/user-attachments/assets/990d5aa2-80f9-458f-add2-a70301d081aa" />


---

**Save and exit**

---

### Step 14: Configure Dovecot for Postfix SASL

**Command:**

```bash
sudo nano /etc/dovecot/conf.d/10-master.conf
```

**Explanation:** Configures Dovecot to provide authentication socket for Postfix.

<img width="1887" height="105" alt="image" src="https://github.com/user-attachments/assets/852c2df6-1cc1-44ca-9fbf-901325d6767a" />

---

**Find the "service auth" section and modify:**

```
service auth {
  unix_listener /var/spool/postfix/private/auth {
    mode = 0660
    user = postfix
    group = postfix
  }
}
```

**Explanation:**

- Creates a Unix socket in Postfix's private directory
- `mode = 0660`: Postfix and Dovecot can read/write
- `user/group = postfix`: Owned by postfix so it can access

<img width="2416" height="1176" alt="image" src="https://github.com/user-attachments/assets/51e9453a-a1f5-45c6-b498-6ce6c387a6cf" />

---

**Save and exit**

---

## Phase 5: Firewall Configuration

### Step 15: Configure Firewalld

**Command:**

```bash
sudo firewall-cmd --list-all
```

**Explanation:** Shows current firewall configuration BEFORE making changes. Use this as a baseline.

<img width="1844" height="914" alt="image" src="https://github.com/user-attachments/assets/85f9fe39-64c9-4e50-ad61-40b2352646b8" />

**What to document:**

- Active zone
- Currently allowed services
- Currently allowed ports

---

**Command:**

```bash
sudo firewall-cmd --permanent --add-service=smtp
```

**Explanation:** Opens port 25 (SMTP) for incoming connections. The `--permanent` flag makes this survive reboots.

<img width="2002" height="242" alt="image" src="https://github.com/user-attachments/assets/8c810b22-8638-4e65-a29a-986aa99a51bd" />

---

**Command:**

```bash
sudo firewall-cmd --permanent --add-service=smtps
```

**Explanation:** Opens port 465 (SMTPS - SMTP over TLS)

<img width="2017" height="183" alt="image" src="https://github.com/user-attachments/assets/fa796950-a05e-4462-b5e2-87b1590e5c87" />

---

**Command:**

```bash
sudo firewall-cmd --permanent --add-port=587/tcp
```

**Explanation:** Opens port 587 (Submission - SMTP with STARTTLS). We use `add-port` because the "submission" service name is often not defined by default on Rocky Linux.

<img width="1961" height="262" alt="image" src="https://github.com/user-attachments/assets/fb524ff7-7036-49fd-8ad7-09d70dae2ee1" />

---

**Command:**

```bash
sudo firewall-cmd --permanent --add-port=143/tcp
```

**Explanation:** Opens port 143 (IMAP) for mail retrieval.

<img width="1971" height="220" alt="image" src="https://github.com/user-attachments/assets/2ee1c504-f7b9-4a0d-81e2-ad03b8752b1d" />

---

**Command:**

```bash
sudo firewall-cmd --permanent --add-port=993/tcp
```

**Explanation:** Opens port 993 (IMAPS - IMAP over TLS).

<img width="1964" height="172" alt="image" src="https://github.com/user-attachments/assets/923b0eca-226f-4629-98b1-434d669f8c53" />

---

**Command:**

```bash
sudo firewall-cmd --reload
```

**Explanation:** Reloads the firewall configuration to apply all the permanent changes we just made.

<img width="1344" height="201" alt="image" src="https://github.com/user-attachments/assets/79afe2bd-9a8a-4c1c-b69c-9958858c711f" />

---

**Command:**

```bash
sudo firewall-cmd --list-all
```

**Explanation:** Verify all the services were added to the firewall.

<img width="2113" height="892" alt="image" src="https://github.com/user-attachments/assets/24801f6a-ea65-42a1-847d-aa68b564a267" />

**What to document:**

- Compare to the "before" screenshot
- Highlight the new services (smtp, smtps) and ports (587, 143, 993) added

---

## Phase 6: Start and Enable Services

### Step 16: Start Postfix

**Command:**

```bash
sudo systemctl start postfix
```

**Explanation:** Starts the Postfix mail server service. This doesn't enable it to auto-start on boot yet.

<img width="1403" height="211" alt="image" src="https://github.com/user-attachments/assets/5cfc0a7a-046c-4f05-b3a2-e5a693f4780c" />

---

**Command:**

```bash
sudo systemctl status postfix
```

**Explanation:** Checks if Postfix is running and shows recent log entries.

<img width="2538" height="1243" alt="image" src="https://github.com/user-attachments/assets/cadcfebd-7a97-45b2-ae95-283070d4ff01" />

**What to document:**

- "Active: active (running)" in green
- Process ID (PID)
- Recent log lines
- No errors

---

**Command:**

```bash
sudo systemctl enable postfix
```

**Explanation:** Configures Postfix to automatically start when the system boots.

<img width="2535" height="219" alt="image" src="https://github.com/user-attachments/assets/64912f22-b383-40be-890f-95861843a7af" />

---

### Step 17: Start Dovecot

**Command:**

```bash
sudo systemctl start dovecot
```

**Explanation:** Starts the Dovecot IMAP server.

<img width="1451" height="221" alt="image" src="https://github.com/user-attachments/assets/bcfa87a8-d66d-45e8-8f4c-a8bb9e80f8a2" />

---

**Command:**

```bash
sudo systemctl status dovecot
```

**Explanation:** Verifies Dovecot is running.

<img width="2537" height="1230" alt="image" src="https://github.com/user-attachments/assets/a6bc8901-1216-4a76-9af8-d72c668f7745" />

**What to document:**

- Active status
- PID
- Log entries
- No SSL/TLS errors

---

**Command:**

```bash
sudo systemctl enable dovecot
```

**Explanation:** Enable Dovecot to auto-start on boot.

<img width="2530" height="286" alt="image" src="https://github.com/user-attachments/assets/7c120649-aa1a-48a5-a5cb-cad56e253b98" />

---

## Phase 7: Verification

### Step 18: Verify Listening Ports

**Command:**

```bash
ss -tuln | grep -E '25|465|587|143|993'
```

**Explanation:** Shows all listening TCP/UDP ports and filters for our mail ports:

- 25 (SMTP)
- 465 (SMTPS)
- 587 (Submission)
- 143 (IMAP)
- 993 (IMAPS)

<img width="1807" height="759" alt="image" src="https://github.com/user-attachments/assets/154a322b-9e07-442d-b773-ee95699c1a12" />

**What to document:**

- All 5 ports showing as LISTEN
- The IP addresses they're bound to (should be 0.0.0.0 or specific IP)

---

**Command:**

```bash
sudo netstat -tlnp | grep -E 'postfix|dovecot'
```

**Explanation:** Shows which processes are listening on which ports, filtered for postfix and dovecot.

<img width="2381" height="545" alt="image" src="https://github.com/user-attachments/assets/f7ae68be-341b-4e26-ae30-a1bee332a4e4" />

---

### Step 19: Test Local SMTP (Port 25)

**Command:**

```bash
telnet localhost 25
```

**Explanation:** Connects to the SMTP service on port 25 locally to test basic connectivity.

<img width="1151" height="405" alt="image" src="https://github.com/user-attachments/assets/ebec60d6-2196-4257-a30f-717ee0a61874" />

**Expected Output:**

```
220 bnaserver.bungkus.org ESMTP Postfix
```

**What to document:**

- 220 status code
- Your hostname in the banner
- Type `QUIT` to exit

---

### Step 20: Test SMTP with STARTTLS

**Command:**

```bash
openssl s_client -connect localhost:25 -starttls smtp
```

**Explanation:** Tests SMTP with STARTTLS encryption:

- Connects to port 25
- Issues STARTTLS command
- Shows SSL/TLS handshake details
- Verifies certificate

<img width="2164" height="1487" alt="image" src="https://github.com/user-attachments/assets/f6dfbb22-2360-42fa-b2e3-8208d9d8dc6a" />

**What to document:**

- "CONNECTED" message
- Certificate subject (should show CN=bnaserver.bungkus.org)
- Verify return code
- "250" SMTP responses

**Type `QUIT` and Enter to exit**

---

### Step 21: Test SMTPS (Port 465)

**Command:**

```bash
openssl s_client -connect localhost:465
```

**Explanation:** Tests SMTPS (immediate TLS on port 465). No STARTTLS needed, connection is encrypted from the start.

<img width="1736" height="65" alt="image" src="https://github.com/user-attachments/assets/0997a582-45e0-41b0-b230-d7a5ea526889" />

<img width="2217" height="1462" alt="image" src="https://github.com/user-attachments/assets/87f3830c-31f7-40fb-9a9d-33ba02cb175d" />

**What to document:**

- Successful TLS connection
- 220 Postfix banner

**Type `QUIT` and Enter to exit**

---

### Step 22: Test Submission (Port 587)

**Command:**

```bash
openssl s_client -connect localhost:587 -starttls smtp
```

<img width="2121" height="74" alt="image" src="https://github.com/user-attachments/assets/7ade5b82-6d1a-4500-9f25-5ecf2b702624" />

<img width="2239" height="1499" alt="image" src="https://github.com/user-attachments/assets/d8697ec3-8862-4783-bab8-713576c083a7" />

**Type `QUIT` and Enter to exit**

---

### Step 23: Test IMAPS (Port 993)

**Command:**

```bash
openssl s_client -connect localhost:993
```

**Explanation:** Tests IMAPS (IMAP over TLS on port 993). Should show Dovecot banner.

<img width="1793" height="156" alt="image" src="https://github.com/user-attachments/assets/3e418311-ae14-4b21-8c18-701c9749c7e6" />

<img width="2527" height="247" alt="image" src="https://github.com/user-attachments/assets/5c722b3f-0b14-4c8c-849b-9886065773bc" />


**Expected Output:**

```
* OK [CAPABILITY IMAP4rev1 ...] Dovecot ready.
```

**What to document:**

- TLS connection success
- Dovecot banner
- CAPABILITY list

**Type `A1 LOGOUT` and Enter to exit**

---

### Step 24: Send Test Email Locally

**Command:**

```bash
openssl s_client -starttls smtp -connect localhost:25 -quiet
```

**Explanation:** Opens an encrypted SMTP session for sending a test email.

<img width="2297" height="561" alt="image" src="https://github.com/user-attachments/assets/fce10133-719a-4f21-a1e7-389acc3f4bb5" />

---

**Then type these SMTP commands:**

```
EHLO localhost
MAIL FROM:<dineesh@bungkus.org>
RCPT TO:<dineesh@bungkus.org>
DATA
Subject: Test Email from SMTP Lab

This is a test email to verify the mail server is working.
.
QUIT
```

**Explanation of SMTP Commands:**

- `EHLO localhost`: Identify ourselves to the server
- `MAIL FROM`: Who the email is from
- `RCPT TO`: Who to deliver to
- `DATA`: Start message content
- `.` (period alone): End message
- `QUIT`: Close connection

<img width="856" height="741" alt="image" src="https://github.com/user-attachments/assets/1a4e170e-a249-42ab-a031-94411f15f9e2" />

<img width="1733" height="650" alt="image" src="https://github.com/user-attachments/assets/57b2eeb8-aec2-4ee8-8936-ea4ab1b815fa" />


**What to document:**

- Each command entered
- 250 responses (success)
- Queue ID from the "250 2.0.0 Ok: queued as XXXXX" message

---

### Step 25: Verify Email Was Queued

**Command:**

```bash
sudo mailq
```

**Explanation:** Shows the mail queue. If email was delivered locally, queue should be empty. If it's still being processed, you'll see it here.

<img width="957" height="196" alt="image" src="https://github.com/user-attachments/assets/15dc6a2a-7bed-41f3-83c4-e245d97fce14" />

---

**Command:**

```bash
sudo tail -20 /var/log/maillog
```

**Explanation:** Shows the last 20 lines of the mail server log to see the email delivery.

<img width="1796" height="151" alt="image" src="https://github.com/user-attachments/assets/69a969fd-484a-4204-8e7f-13b5bff8a50d" />

<img width="2537" height="940" alt="image" src="https://github.com/user-attachments/assets/45283334-2011-4259-bd2f-bf84cdac5572" />


**What to document:**

- "queued as" entry
- "status=sent" entry (if delivered)
- Any errors

---

### Step 26: Retrieve Email via IMAP

**Command:**

```bash
openssl s_client -connect localhost:993 -quiet
```

**Explanation:** Opens encrypted IMAP connection to retrieve the test email.

<img width="1969" height="123" alt="image" src="https://github.com/user-attachments/assets/d1311f68-abf2-4313-aa0e-3020a8009565" />

---

**IMAP Commands:**

```
A1 LOGIN dineesh Lab2026
A2 SELECT INBOX
A3 FETCH 1 BODY[]
A4 LOGOUT
```

**Explanation:**

- `A1 LOGIN`: Authenticate as user "dineesh"
- `A2 SELECT INBOX`: Open the inbox folder
- `A3 FETCH 1 BODY[]`: Retrieve full body of message 1
- `A4 LOGOUT`: Close connection


**What to document:**

- Login success (A1 OK)
- Inbox selected showing message count
- Full email content including your test message
- Logout confirmation

---

## 🎉 Rocky Server Setup Complete

Your Rocky Linux mail server is now fully configured and tested!

---

# PART 2: UBUNTU CLIENT SETUP

## Phase 8: Ubuntu Client Configuration

### Step 27: Configure Hosts File on Ubuntu

**Command:**

```bash
sudo nano /etc/hosts
```

**Explanation:** Opens Ubuntu's hosts file to add the mail server entry.

**📸 [TAKE SCREENSHOT]** - Show nano opened

---

**Add this line:**

```
192.168.200.3 bnaserver.bungkus.org
```

**Explanation:** Tells Ubuntu where to find the mail server by mapping the hostname to the IP address.

**📸 [TAKE SCREENSHOT]** - Show edited hosts file

**Save and exit**

---

**Command:**

```bash
cat /etc/hosts
```

**Explanation:** Verify the entry was saved.

**📸 [TAKE SCREENSHOT]** - Show hosts file with new entry

---

### Step 27: Test Connectivity to Mail Server

**Command:**

```bash
ping -c 3 bnaserver.bungkus.org
```

**Explanation:** Verify name resolution and network connectivity to the mail server.

**📸 [TAKE SCREENSHOT]** - Show ping results

**What to document:**

- IP address resolved (should be 192.168.200.3)
- Packets received (0% loss)
- Round trip times

---

**Command:**

```bash
telnet bnaserver.bungkus.org 25
```

**Explanation:** Test TCP connectivity to SMTP port 25.

**📸 [TAKE SCREENSHOT]** - Show connection and Postfix banner

**What to document:**

- Connection established
- 220 banner from mail server
- Type `QUIT` to exit

---

**Command:**

```bash
openssl s_client -connect bnaserver.bungkus.org:993
```

**Explanation:** Test encrypted connection to IMAPS port 993 and verify the SSL certificate.

**📸 [TAKE SCREENSHOT]** - Show TLS connection and certificate

**What to document:**

- "CONNECTED" status
- Certificate subject (CN=bnaserver.bungkus.org)
- Dovecot ready message
- Type `A1 LOGOUT` to exit

---

## Phase 9: Thunderbird Installation

### Step 28: Download Thunderbird

**If using browser:**
Visit: <https://www.thunderbird.net/>

**📸 [TAKE SCREENSHOT]** - Show download page

---

**If using wget:**

```bash
cd ~/Downloads
wget https://download.mozilla.org/?product=thunderbird-latest-ssl&os=linux64&lang=en-US -O thunderbird.tar.bz2
```

**Explanation:** Downloads the latest Thunderbird directly to your Downloads folder.

**📸 [TAKE SCREENSHOT]** - Show download progress

---

### Step 29: Extract Thunderbird

**Command:**

```bash
cd ~/Downloads
tar -xvf thunderbird*.tar.bz2
```

**Explanation:** Extracts the Thunderbird archive. The `*` wildcard matches any version number.

**📸 [TAKE SCREENSHOT]** - Show extraction process

**What to document:**

- Files being extracted
- "thunderbird" folder created

---

**Command:**

```bash
ls -la thunderbird/
```

**Explanation:** Lists contents of extracted Thunderbird folder to verify extraction was successful.

**📸 [TAKE SCREENSHOT]** - Show Thunderbird directory contents

---

### Step 30: Install Thunderbird

**Command:**

```bash
sudo mv thunderbird /opt/
```

**Explanation:** Moves Thunderbird to /opt/ directory (standard location for third-party applications in Linux).

**📸 [TAKE SCREENSHOT]** - Show move command

---

**Command:**

```bash
sudo ln -sf /opt/thunderbird/thunderbird /usr/bin/thunderbird
```

**Explanation:** Creates a symbolic link so you can run "thunderbird" from anywhere in the terminal.

- `-s`: Create symbolic link
- `-f`: Force (overwrite if exists)

**📸 [TAKE SCREENSHOT]** - Show symlink creation

---

**Command:**

```bash
which thunderbird
```

**Explanation:** Verifies the symlink is working and shows the path.

**📸 [TAKE SCREENSHOT]** - Show output: /usr/bin/thunderbird

---

### Step 31: Launch Thunderbird

**Command:**

```bash
thunderbird &
```

**Explanation:** Launches Thunderbird in the background (& symbol). The terminal remains usable.

**📸 [TAKE SCREENSHOT]** - Show Thunderbird welcome screen

---

## Phase 10: Thunderbird Email Account Configuration

### Step 32: Add Mail Account

**In Thunderbird:**

1. Click "Set up an account" or "Email"
2. Enter:
   - **Your name:** dineesh
   - **Email address:** <dineesh@bungkus.org>
   - **Password:** Lab2026

**📸 [TAKE SCREENSHOT]** - Show account setup form filled in

---

1. Click "Continue"
2. Thunderbird will try auto-detection (it will fail - that's expected)

**📸 [TAKE SCREENSHOT]** - Show "Could not find settings" or similar message

---

### Step 33: Manual Configuration

1. Click "Manual config" or "Configure manually"

**📸 [TAKE SCREENSHOT]** - Show manual configuration screen

---

1. Enter these settings:

**Incoming (IMAP):**

- **Server hostname:** bnaserver.bungkus.org (or 192.168.200.3)
- **Port:** 993
- **SSL:** SSL/TLS
- **Authentication:** Normal password
- **Username:** dineesh

**Outgoing (SMTP):**

- **Server hostname:** bnaserver.bungkus.org (or 192.168.200.3)
- **Port:** 465
- **SSL:** SSL/TLS
- **Authentication:** Normal password
- **Username:** dineesh

**📸 [TAKE SCREENSHOT]** - Show all manual configuration settings

**What to document:**

- All fields filled correctly
- Port numbers
- SSL/TLS selected
- Username is "dineesh" NOT "<dineesh@bungkus.org>"

---

### Step 34: Disable OCSP (Critical!)

**Before clicking "Done":**

1. Open Settings (Hamburger menu → Settings)
2. Search for "OCSP"
3. **UNCHECK** "Query OCSP responder servers to confirm validity of certificates"

**📸 [TAKE SCREENSHOT]** - Show OCSP option unchecked

**Explanation:** Self-signed certificates can't be validated via OCSP, causing Thunderbird to hang indefinitely. Disabling OCSP prevents this.

---

### Step 35: Security Exception

1. Go back to account setup and click "Done"
2. A certificate warning will appear

**📸 [TAKE SCREENSHOT]** - Show certificate warning dialog

---

1. Click "Confirm Security Exception" or "Add Exception"

**📸 [TAKE SCREENSHOT]** - Show security exception confirmation

**What to document:**

- Certificate details showing CN=bnaserver.bungkus.org
- Check "Permanently store this exception"

---

### Step 36: Verify Connection Success

**📸 [TAKE SCREENSHOT]** - Show Thunderbird main window with account connected

**What to document:**

- Account "<dineesh@bungkus.org>" in left panel
- Inbox visible
- Your test email from earlier should appear!

---

### Step 37: View Test Email

Click on the test email in the inbox.

**📸 [TAKE SCREENSHOT]** - Show email content displayed

**What to document:**

- Subject: "Test Email from SMTP Lab"
- Full email body
- From/To headers

---

### Step 38: Send Test Email from Thunderbird

1. Click "Write" (new message)
2. Fill in:
   - **To:** <dineesh@bungkus.org>
   - **Subject:** Test from Thunderbird
   - **Body:** Testing SMTP send from Thunderbird client

**📸 [TAKE SCREENSHOT]** - Show compose window

---

1. Click "Send"

**📸 [TAKE SCREENSHOT]** - Show email being sent

---

1. Wait a few seconds, check inbox for the new message

**📸 [TAKE SCREENSHOT]** - Show new email received

**What to document:**

- Email sent successfully
- Email appears in inbox
- Sent folder shows copy of sent message

---

## 🎊 LAB COMPLETE

You have successfully:

- ✅ Configured a complete Postfix + Dovecot mail server on Rocky Linux
- ✅ Generated and configured SSL/TLS certificates
- ✅ Configured all SMTP ports (25, 465, 587) and IMAP ports (143, 993)
- ✅ Set up client on Ubuntu
- ✅ Connected Thunderbird with SSL/TLS
- ✅ Sent and received encrypted email

---

## 📝 Documentation Checklist

Make sure you have screenshots of:

- [ ] Every command listed in this guide
- [ ] Configuration files open in editors
- [ ] Service status outputs
- [ ] Port verification
- [ ] Test email send/receive
- [ ] Thunderbird configuration screens
- [ ] Certificate warnings and exceptions
- [ ] Final working email

---

## 💡 For Your Report

For each screenshot, add a caption that includes:

1. **Command/Action:** What command was run or button clicked
2. **Purpose:** Why this step is necessary
3. **Result:** What the output shows or what happened
4. **Notes:** Any important observations

**Example:**

```
Screenshot 23: Testing SMTP Connection with STARTTLS

Command: openssl s_client -connect localhost:25 -starttls smtp

Purpose: This command tests the SMTP service on port 25 and verifies that 
STARTTLS encryption is working properly. It establishes a TLS connection 
and shows the SSL certificate details.

Result: The output shows "CONNECTED(00000003)" indicating successful TCP 
connection, followed by the TLS handshake details and a "250" response from 
Postfix, confirming the server is accepting secure connections.

Notes: The certificate subject shows "CN=bnaserver.bungkus.org" which 
matches our hostname, confirming the certificate was generated correctly.
```

---

**Good luck with your lab documentation! You've got this! 🚀**

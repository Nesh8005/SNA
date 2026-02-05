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

**📸 [TAKE SCREENSHOT]** - Show the command and the prompts for password/user info

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

**📸 [TAKE SCREENSHOT]** - Show entering password (characters will be hidden)

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

**📸 [TAKE SCREENSHOT]** - Show the command (no output is normal)

---

**Command:**

```bash
hostnamectl
```

**Explanation:** Verifies the hostname was set correctly. This displays system information including the static hostname, which should now be "bnaserver.bungkus.org".

**📸 [TAKE SCREENSHOT]** - Show full output with hostname details

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

**📸 [TAKE SCREENSHOT]** - Show command and output

**Expected Output:** `bnaserver.bungkus.org`

---

### Step 3: Configure Hosts File

**Command:**

```bash
sudo nano /etc/hosts
```

**Explanation:** Opens the hosts file for editing. This file maps IP addresses to hostnames locally, allowing the server to resolve its own hostname without DNS.

**📸 [TAKE SCREENSHOT]** - Show nano editor opened

---

**What to Add:**

```
192.168.200.3 bnaserver.bungkus.org bnaserver
```

**Explanation:** This entry tells the server:

- "When you see bnaserver.bungkus.org or bnaserver, use IP 192.168.200.3"
- This is essential for the mail server to identify itself correctly
- Without this, services may fail to start or malfunction

**📸 [TAKE SCREENSHOT]** - Show the edited hosts file with the new line added

**What to document:**

- The complete /etc/hosts file with your addition
- Highlight the line you added

---

**Command to Save:**

- Press `Ctrl + O` (WriteOut)
- Press `Enter` (Confirm filename)
- Press `Ctrl + X` (Exit)

**📸 [TAKE SCREENSHOT]** - Show the save confirmation at bottom of screen

---

**Command:**

```bash
cat /etc/hosts
```

**Explanation:** Displays the contents of the hosts file to verify your changes were saved correctly.

**📸 [TAKE SCREENSHOT]** - Show the hosts file contents

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

**📸 [TAKE SCREENSHOT]** - Show full output

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

**📸 [TAKE SCREENSHOT]** - Show routing table

**What to document:**

- Default route via 192.168.200.2
- Local network route

**🚨 IMPORTANT:** If you don't see "default via 192.168.200.2", you need to add it!

---

**Command (if gateway is missing):**

```bash
sudo ip route add default via 192.168.200.2 dev enp0s3
```

**Explanation:** Manually adds the default gateway to the routing table. Replace "enp0s3" with your actual interface name from `ip addr show`. This tells the server where to send traffic destined for the internet.

**📸 [TAKE SCREENSHOT]** - Show command execution (only if needed)

---

**Command:**

```bash
ping -c 3 8.8.8.8
```

**Explanation:** Tests internet connectivity by pinging Google's DNS server. Sends 3 ICMP packets and waits for replies.

**📸 [TAKE SCREENSHOT]** - Show ping results

**What to document:**

- Whether packets are received (success) or lost (failure)
- Round-trip time
- Note: In VirtualBox NAT, this MIGHT fail even when internet works!

---

**Command:**

```bash
curl -I https://google.com
```

**Explanation:** Tests HTTP/HTTPS connectivity by fetching headers from Google. This is a more reliable internet test than ping in VirtualBox environments.

**📸 [TAKE SCREENSHOT]** - Show HTTP headers received

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

**📸 [TAKE SCREENSHOT]** - Show update process (beginning and end)

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

**📸 [TAKE SCREENSHOT]** - Show installation process

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

**📸 [TAKE SCREENSHOT]** - Show installed postfix package

**Expected Output:** `postfix-3.x.x-x.el9.x86_64` (version numbers may vary)

---

**Command:**

```bash
rpm -qa | grep dovecot
```

**Explanation:** Verifies Dovecot installation the same way as above.

**📸 [TAKE SCREENSHOT]** - Show installed dovecot packages

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

**📸 [TAKE SCREENSHOT]** - Show command execution

**Expected Output:** Usually no output means success

---

**Command:**

```bash
sudo ls -l /etc/pki/tls/certs/bnaserver.pem
```

**Explanation:** Verifies the certificate file was created and shows its permissions and size.

**📸 [TAKE SCREENSHOT]** - Show file details

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

**📸 [TAKE SCREENSHOT]** - Show file details

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

**📸 [TAKE SCREENSHOT]** - Show command and permissions after

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

**📸 [TAKE SCREENSHOT]** - Show command

---

**Command:**

```bash
sudo openssl x509 -in /etc/pki/tls/certs/bnaserver.pem -text -noout
```

**Explanation:** Displays the certificate details in human-readable format without showing the encoded certificate data. Use this to verify:

- The Common Name (CN) matches your hostname
- Validity dates
- Signature algorithm

**📸 [TAKE SCREENSHOT]** - Show certificate details

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

**📸 [TAKE SCREENSHOT]** - Show command

---

**Command:**

```bash
ls -l /etc/postfix/main.cf*
```

**Explanation:** Lists both the original and backup configuration files to verify the backup was created.

**📸 [TAKE SCREENSHOT]** - Show both files listed

---

### Step 9: Edit Postfix Main Configuration

**Command:**

```bash
sudo nano /etc/postfix/main.cf
```

**Explanation:** Opens the main Postfix configuration file for editing. This file controls all SMTP server behavior.

**📸 [TAKE SCREENSHOT]** - Show nano editor opened with main.cf

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

**📸 [TAKE SCREENSHOT]** - Show the edited main.cf with all these settings

**What to document:**

- Scroll through and capture all the sections you modified
- Highlight the key changes

---

**Save and Exit:**

- Ctrl+O (save)
- Enter (confirm)
- Ctrl+X (exit)

**📸 [TAKE SCREENSHOT]** - Show save confirmation

---

**Command:**

```bash
sudo postconf -n
```

**Explanation:** Displays only the non-default settings in Postfix configuration (excludes all the commented default values). This makes it easy to see what you've actually changed.

**📸 [TAKE SCREENSHOT]** - Show your custom configuration

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

**📸 [TAKE SCREENSHOT]** - Show backup command

---

**Command:**

```bash
sudo nano /etc/postfix/master.cf
```

**Explanation:** Opens the Postfix master configuration file which controls which services run on which ports.

**📸 [TAKE SCREENSHOT]** - Show nano opened

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

**📸 [TAKE SCREENSHOT]** - Show submission configuration

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

**📸 [TAKE SCREENSHOT]** - Show smtps configuration

---

**Save and Exit nano**

**📸 [TAKE SCREENSHOT]** - Show save confirmation

---

## Phase 4: Dovecot Configuration

### Step 11: Configure Dovecot SSL

**Command:**

```bash
sudo nano /etc/dovecot/conf.d/10-ssl.conf
```

**Explanation:** Opens Dovecot's SSL configuration file where we specify certificate paths and SSL requirements.

**📸 [TAKE SCREENSHOT]** - Show file opened

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

**📸 [TAKE SCREENSHOT]** - Show SSL configuration

---

**Save and exit**

**📸 [TAKE SCREENSHOT]** - Show save

---

### Step 12: Configure Dovecot Authentication

**Command:**

```bash
sudo nano /etc/dovecot/conf.d/10-auth.conf
```

**Explanation:** Configures how Dovecot authenticates users (using system accounts).

**📸 [TAKE SCREENSHOT]** - Show file opened

---

**Find and verify/modify:**

```
disable_plaintext_auth = yes
auth_mechanisms = plain login
```

**Explanation:**

- `disable_plaintext_auth = yes`: Don't allow passwords over unencrypted connections
- `auth_mechanisms = plain login`: Allow PLAIN and LOGIN auth methods (over TLS)

**📸 [TAKE SCREENSHOT]** - Show auth configuration

---

**Save and exit**

---

### Step 13: Configure Dovecot for Postfix SASL

**Command:**

```bash
sudo nano /etc/dovecot/conf.d/10-master.conf
```

**Explanation:** Configures Dovecot to provide authentication socket for Postfix.

**📸 [TAKE SCREENSHOT]** - Show file opened

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

**📸 [TAKE SCREENSHOT]** - Show service auth configuration

---

**Save and exit**

---

## Phase 5: Firewall Configuration

### Step 14: Configure Firewalld

**Command:**

```bash
sudo firewall-cmd --list-all
```

**Explanation:** Shows current firewall configuration BEFORE making changes. Use this as a baseline.

**📸 [TAKE SCREENSHOT]** - Show current firewall state

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

**📸 [TAKE SCREENSHOT]** - Show command and "success" output

---

**Command:**

```bash
sudo firewall-cmd --permanent --add-service=smtps
```

**Explanation:** Opens port 465 (SMTPS - SMTP over TLS)

**📸 [TAKE SCREENSHOT]** - Show command

---

**Command:**

```bash
sudo firewall-cmd --permanent --add-service=submission
```

**Explanation:** Opens port 587 (Submission - SMTP with STARTTLS)

**📸 [TAKE SCREENSHOT]** - Show command

---

**Command:**

```bash
sudo firewall-cmd --permanent --add-service=imap
```

**Explanation:** Opens port 143 (IMAP) for mail retrieval

**📸 [TAKE SCREENSHOT]** - Show command

---

**Command:**

```bash
sudo firewall-cmd --permanent --add-service=imaps
```

**Explanation:** Opens port 993 (IMAPS - IMAP over TLS)

**📸 [TAKE SCREENSHOT]** - Show command

---

**Command:**

```bash
sudo firewall-cmd --reload
```

**Explanation:** Reloads the firewall configuration to apply all the permanent changes we just made.

**📸 [TAKE SCREENSHOT]** - Show reload success

---

**Command:**

```bash
sudo firewall-cmd --list-all
```

**Explanation:** Verify all the services were added to the firewall.

**📸 [TAKE SCREENSHOT]** - Show NEW firewall state with all services

**What to document:**

- Compare to the "before" screenshot
- Highlight the 5 new services added

---

## Phase 6: Start and Enable Services

### Step 15: Start Postfix

**Command:**

```bash
sudo systemctl start postfix
```

**Explanation:** Starts the Postfix mail server service. This doesn't enable it to auto-start on boot yet.

**📸 [TAKE SCREENSHOT]** - Show command (no output = success)

---

**Command:**

```bash
sudo systemctl status postfix
```

**Explanation:** Checks if Postfix is running and shows recent log entries.

**📸 [TAKE SCREENSHOT]** - Show full status output

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

**📸 [TAKE SCREENSHOT]** - Show command and symlink creation message

---

### Step 16: Start Dovecot

**Command:**

```bash
sudo systemctl start dovecot
```

**Explanation:** Starts the Dovecot IMAP server.

**📸 [TAKE SCREENSHOT]** - Show command

---

**Command:**

```bash
sudo systemctl status dovecot
```

**Explanation:** Verifies Dovecot is running.

**📸 [TAKE SCREENSHOT]** - Show full status with "active (running)"

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

**📸 [TAKE SCREENSHOT]** - Show enable command

---

## Phase 7: Verification

### Step 17: Verify Listening Ports

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

**📸 [TAKE SCREENSHOT]** - Show all 5 ports in LISTEN state

**What to document:**

- All 5 ports showing as LISTEN
- The IP addresses they're bound to (should be 0.0.0.0 or specific IP)

---

**Command:**

```bash
sudo netstat -tlnp | grep -E 'postfix|dovecot'
```

**Explanation:** Shows which processes are listening on which ports, filtered for postfix and dovecot.

**📸 [TAKE SCREENSHOT]** - Show postfix and dovecot processes with their ports

---

### Step 18: Test Local SMTP (Port 25)

**Command:**

```bash
telnet localhost 25
```

**Explanation:** Connects to the SMTP service on port 25 locally to test basic connectivity.

**📸 [TAKE SCREENSHOT]** - Show connection established and banner

**Expected Output:**

```
220 bnaserver.bungkus.org ESMTP Postfix
```

**What to document:**

- 220 status code
- Your hostname in the banner
- Type `QUIT` to exit

---

### Step 19: Test SMTP with STARTTLS

**Command:**

```bash
openssl s_client -connect localhost:25 -starttls smtp
```

**Explanation:** Tests SMTP with STARTTLS encryption:

- Connects to port 25
- Issues STARTTLS command
- Shows SSL/TLS handshake details
- Verifies certificate

**📸 [TAKE SCREENSHOT]** - Show TLS handshake success and certificate details

**What to document:**

- "CONNECTED" message
- Certificate subject (should show CN=bnaserver.bungkus.org)
- Verify return code
- "250" SMTP responses

**Type `QUIT` and Enter to exit**

---

### Step 20: Test SMTPS (Port 465)

**Command:**

```bash
openssl s_client -connect localhost:465
```

**Explanation:** Tests SMTPS (immediate TLS on port 465). No STARTTLS needed, connection is encrypted from the start.

**📸 [TAKE SCREENSHOT]** - Show connection and Postfix banner over TLS

**What to document:**

- Successful TLS connection
- 220 Postfix banner

**Type `QUIT` and Enter to exit**

---

### Step 21: Test Submission (Port 587)

**Command:**

```bash
openssl s_client -connect localhost:587 -starttls smtp
```

**Explanation:** Tests the submission port (587) with STARTTLS.

**📸 [TAKE SCREENSHOT]** - Show successful connection

**Type `QUIT` and Enter to exit**

---

### Step 22: Test IMAPS (Port 993)

**Command:**

```bash
openssl s_client -connect localhost:993
```

**Explanation:** Tests IMAPS (IMAP over TLS on port 993). Should show Dovecot banner.

**📸 [TAKE SCREENSHOT]** - Show Dovecot ready message

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

### Step 23: Send Test Email Locally

**Command:**

```bash
openssl s_client -starttls smtp -connect localhost:25 -quiet
```

**Explanation:** Opens an encrypted SMTP session for sending a test email.

**📸 [TAKE SCREENSHOT]** - Show connection established

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

**📸 [TAKE SCREENSHOT]** - Show all commands and "250 OK" responses

**What to document:**

- Each command entered
- 250 responses (success)
- Queue ID from the "250 2.0.0 Ok: queued as XXXXX" message

---

### Step 24: Verify Email Was Queued

**Command:**

```bash
sudo mailq
```

**Explanation:** Shows the mail queue. If email was delivered locally, queue should be empty. If it's still being processed, you'll see it here.

**📸 [TAKE SCREENSHOT]** - Show mail queue status

---

**Command:**

```bash
sudo tail -20 /var/log/maillog
```

**Explanation:** Shows the last 20 lines of the mail server log to see the email delivery.

**📸 [TAKE SCREENSHOT]** - Show log entries for your test email

**What to document:**

- "queued as" entry
- "status=sent" entry (if delivered)
- Any errors

---

### Step 25: Retrieve Email via IMAP

**Command:**

```bash
openssl s_client -connect localhost:993 -quiet
```

**Explanation:** Opens encrypted IMAP connection to retrieve the test email.

**📸 [TAKE SCREENSHOT]** - Show Dovecot ready

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

**📸 [TAKE SCREENSHOT]** - Show successful login and email retrieval

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

### Step 26: Configure Hosts File on Ubuntu

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



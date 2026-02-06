# Postfix & Dovecot Mail Server Implementation Guide

This document provides a comprehensive, professional guide for deploying a secure SMTP and IMAP mail server on Rocky Linux 9, along with client configuration on Ubuntu.

## System Architecture

* **Mail Transfer Agent (MTA):** Postfix (SMTP/SMTPS)
* **Mail Delivery Agent (MDA):** Dovecot (IMAP/IMAPS)
* **Operating System:** Rocky Linux 9 (Server), Ubuntu 22.04 (Client)
* **Network Configuration:**
  * **Domain:** `bungkus.org`
  * **Server FQDN:** `bnaserver.bungkus.org` (IP: `192.168.200.3`)
  * **Client IP:** `192.168.200.80`

---

## Part 1: Rocky Linux Server Configuration

### 1. User & System Initialization

**Create Service User**
Create a dedicated system user for authentication testing. Mail servers utilize Linux system accounts for user authentication.

```bash
sudo adduser dineesh
```

<img width="1320" height="213" alt="Screenshot 2026-02-05 090259" src="https://github.com/user-attachments/assets/384e72c5-a5a1-42f0-9115-d06b14108052" />

**Set User Password**
Assign a secure password for the user. This credential will be used for SMTP/IMAP authentication.

```bash
sudo passwd dineesh
```

<img width="1569" height="384" alt="Screenshot 2026-02-05 091115" src="https://github.com/user-attachments/assets/b71a21fe-df88-4cf3-8120-29f38dea7112" />

**Configure Hostname**
Set the Fully Qualified Domain Name (FQDN). This is critical for SSL certificate generation and proper mail routing.

```bash
sudo hostnamectl set-hostname bnaserver.bungkus.org
```

<img width="2074" height="184" alt="Screenshot 2026-02-05 091311" src="https://github.com/user-attachments/assets/555efc67-d7bd-4c9e-9fdc-82847b697bbb" />

**Verify Hostname**

```bash
hostnamectl
```

<img width="1523" height="809" alt="Screenshot 2026-02-05 091411" src="https://github.com/user-attachments/assets/47f329a0-9e59-4baf-8e76-5ab1e5d90385" />

### 2. Network Configuration

**Local DNS Mapping**
Edit `/etc/hosts` to ensure the server can resolve its own FQDN without external DNS.

```bash
sudo nano /etc/hosts
```

**Add the following entry:**

```text
192.168.200.3 bnaserver.bungkus.org bnaserver
```

<img width="2226" height="277" alt="Screenshot 2026-02-05 091648" src="https://github.com/user-attachments/assets/839505f1-3441-4693-9332-c8b76dddce1a" />

**Verify Hosts File**

```bash
cat /etc/hosts
```

<img width="2230" height="295" alt="Screenshot 2026-02-05 091824" src="https://github.com/user-attachments/assets/8533d07e-0415-49c0-856f-61e9c0f3ee6e" />

**Verify Network Interface**
Ensure the static IP is correctly assigned.

```bash
ip addr show
```

<img width="2535" height="819" alt="Screenshot 2026-02-05 092005" src="https://github.com/user-attachments/assets/6e3beb8e-8abb-4896-904c-dc7505d93abb" />

**Verify Routing Table**
Ensure a default gateway exists. If missing, it must be added manually.

```bash
ip route
```

<img width="2288" height="264" alt="Screenshot 2026-02-05 092024" src="https://github.com/user-attachments/assets/99c5b36e-b837-4b08-aebc-c4ad0542e444" />

**Connectivity Test**
Verify internet access using `curl`. Note: standard `ping` may fail in VirtualBox NAT environments due to ICMP blocking.

```bash
curl -I https://google.com
```

<img width="2537" height="962" alt="image" src="https://github.com/user-attachments/assets/4e1133e9-ae51-4446-bbe1-ebbb00ac01bb" />

### 3. Package Installation

**Update System**

```bash
sudo dnf update -y
```

<img width="1629" height="1525" alt="image" src="https://github.com/user-attachments/assets/a104f412-28ff-4f0f-b09c-47ceedd0f479" />

**Install Postfix and Dovecot**

```bash
sudo dnf install postfix dovecot -y
```

<img width="2538" height="1494" alt="image" src="https://github.com/user-attachments/assets/52e82512-7dd5-4b52-b4c9-791dc0e029bb" />

### 4. Security Infrastructure (SSL/TLS)

**Generate Self-Signed Certificate**
Create an X.509 certificate valid for 365 days. The Common Name (CN) **must** match the server FQDN.

```bash
sudo openssl req -new -x509 -days 365 -nodes \
  -out /etc/pki/tls/certs/bnaserver.pem \
  -keyout /etc/pki/tls/private/bnaserver.key \
  -subj "/C=MY/ST=KL/L=APU/O=SNA/CN=bnaserver.bungkus.org"
```

<img width="2549" height="1005" alt="image" src="https://github.com/user-attachments/assets/9a3c1a22-c5fc-41e6-9b8b-6fa46f08fd17" />

**Secure Private Key Permissions**
The private key must be readable only by root (0600), while the certificate allows public read access (0644).

```bash
sudo chmod 600 /etc/pki/tls/private/bnaserver.key
sudo chmod 644 /etc/pki/tls/certs/bnaserver.pem
```

<img width="2022" height="153" alt="image" src="https://github.com/user-attachments/assets/2d307ef2-ee57-4948-8d8a-ba706d7ede6c" />

**Verify Certificate Details**

```bash
sudo openssl x509 -in /etc/pki/tls/certs/bnaserver.pem -text -noout
```

<img width="1063" height="1352" alt="image" src="https://github.com/user-attachments/assets/73b35baa-b961-49e0-9f2c-3cbc19ea5a53" />

### 5. Postfix (MTA) Configuration

**Backup Default Configuration**

```bash
sudo cp /etc/postfix/main.cf /etc/postfix/main.cf.backup
```

**Configure `main.cf`**
Edit `/etc/postfix/main.cf` to define domain settings, network controls, and TLS parameters.

```bash
sudo nano /etc/postfix/main.cf
```

**Required Configuration Block:**

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

<img width="2121" height="1414" alt="image" src="https://github.com/user-attachments/assets/2142ce9c-b78d-4628-b88c-057dadf11de0" />

**Configure `master.cf` (Submission & SMTPS)**
Enable ports 587 (Submission) and 465 (SMTPS) in `/etc/postfix/master.cf`.

**Port 587 (Submission) Configuration:**

```text
submission inet n       -       n       -       -       smtpd
  -o syslog_name=postfix/submission
  -o smtpd_tls_security_level=encrypt
  -o smtpd_sasl_auth_enable=yes
  -o smtpd_sasl_type=dovecot
  -o smtpd_sasl_path=private/auth
  -o smtpd_client_restrictions=permit_sasl_authenticated,reject
```

**Port 465 (SMTPS) Configuration:**

```text
smtps     inet  n       -       n       -       -       smtpd
  -o syslog_name=postfix/smtps
  -o smtpd_tls_wrappermode=yes
  -o smtpd_sasl_auth_enable=yes
  -o smtpd_sasl_type=dovecot
  -o smtpd_sasl_path=private/auth
  -o smtpd_client_restrictions=permit_sasl_authenticated,reject
```

<img width="2324" height="379" alt="image" src="https://github.com/user-attachments/assets/543aac53-f963-4b36-ae6c-fb5893dc91df" />

### 6. Dovecot (MDA) Configuration

**Configure Mail Location**
Edit `/etc/dovecot/conf.d/10-mail.conf` to match Postfix's Maildir format.

```bash
# Change mail_location to:
mail_location = maildir:~/Maildir
```

<img width="1057" height="244" alt="image" src="https://github.com/user-attachments/assets/cde6c42b-cbc8-4777-956f-67490ce2ea26" />

**Configure SSL/TLS**
Edit `/etc/dovecot/conf.d/10-ssl.conf` to enforce SSL encryption and point to the certificates generated earlier.

```bash
ssl = required
ssl_cert = </etc/pki/tls/certs/bnaserver.pem
ssl_key = </etc/pki/tls/private/bnaserver.key
ssl_min_protocol = TLSv1.2
```

<img width="2293" height="510" alt="image" src="https://github.com/user-attachments/assets/d8b3e924-35ee-499d-afe4-398182dc978e" />

**Configure Authentication Mechanisms**
Edit `/etc/dovecot/conf.d/10-auth.conf`.

```bash
disable_plaintext_auth = yes
auth_mechanisms = plain login
```

<img width="2173" height="342" alt="image" src="https://github.com/user-attachments/assets/990d5aa2-80f9-458f-add2-a70301d081aa" />

**Configure SASL Socket for Postfix**
Edit `/etc/dovecot/conf.d/10-master.conf` to create the authentication socket Postfix needs.

```bash
service auth {
  unix_listener /var/spool/postfix/private/auth {
    mode = 0660
    user = postfix
    group = postfix
  }
}
```

<img width="2416" height="1176" alt="image" src="https://github.com/user-attachments/assets/51e9453a-a1f5-45c6-b498-6ce6c387a6cf" />

### 7. Firewall Configuration

Configure `firewalld` to allow SMTP and IMAP traffic permanently.

```bash
sudo firewall-cmd --permanent --add-service=smtp
sudo firewall-cmd --permanent --add-service=smtps
sudo firewall-cmd --permanent --add-port=587/tcp
sudo firewall-cmd --permanent --add-port=143/tcp
sudo firewall-cmd --permanent --add-port=993/tcp
sudo firewall-cmd --reload
```

<img width="2113" height="892" alt="image" src="https://github.com/user-attachments/assets/24801f6a-ea65-42a1-847d-aa68b564a267" />

### 8. Service Management

Start and enable both Postfix and Dovecot services.

```bash
sudo systemctl start postfix
sudo systemctl enable postfix
sudo systemctl start dovecot
sudo systemctl enable dovecot
```

<img width="2538" height="1243" alt="image" src="https://github.com/user-attachments/assets/cadcfebd-7a97-45b2-ae95-283070d4ff01" />

---

## Part 2: Verification & Testing

### 1. Port Verification

Ensure all required ports (25, 465, 587, 143, 993) are in listening state.

```bash
ss -tuln | grep -E '25|465|587|143|993'
```

<img width="1807" height="759" alt="image" src="https://github.com/user-attachments/assets/154a322b-9e07-442d-b773-ee95699c1a12" />

### 2. Local SMTP Test

Test basic SMTP connectivity on port 25 using telnet.

```bash
telnet localhost 25
```

*Expected Response: 220 bnaserver.bungkus.org ESMTP Postfix*

<img width="1151" height="405" alt="image" src="https://github.com/user-attachments/assets/ebec60d6-2196-4257-a30f-717ee0a61874" />

### 3. Encrypted SMTP Test (STARTTLS)

Verify STARTTLS capability on port 25.

```bash
openssl s_client -connect localhost:25 -starttls smtp
```

<img width="2164" height="1487" alt="image" src="https://github.com/user-attachments/assets/f6dfbb22-2360-42fa-b2e3-8208d9d8dc6a" />

### 4. SMTPS Test (Port 465)

Verify dedicated SSL connectivity.

```bash
openssl s_client -connect localhost:465
```

<img width="2217" height="1462" alt="image" src="https://github.com/user-attachments/assets/87f3830c-31f7-40fb-9a9d-33ba02cb175d" />

### 5. IMAPS Test (Port 993)

Verify plain IMAP over SSL.

```bash
openssl s_client -connect localhost:993
```

<img width="2527" height="247" alt="image" src="https://github.com/user-attachments/assets/5c722b3f-0b14-4c8c-849b-9886065773bc" />

### 6. End-to-End Delivery Test

Send a manual test email via the command line and verify delivery to the Maildir.

```bash
openssl s_client -starttls smtp -connect localhost:25 -quiet
```

**SMTP Commands:**

```text
EHLO localhost
MAIL FROM:<dineesh@bungkus.org>
RCPT TO:<dineesh@bungkus.org>
DATA
Subject: Test Email from SMTP Lab

This is a test email to verify the mail server is working.
.
QUIT
```

<img width="1733" height="650" alt="image" src="https://github.com/user-attachments/assets/57b2eeb8-aec2-4ee8-8936-ea4ab1b815fa" />

**Verify Delivery:**
Check the mail queue and logs.

```bash
sudo mailq
sudo tail -20 /var/log/maillog
```

<img width="2537" height="940" alt="image" src="https://github.com/user-attachments/assets/45283334-2011-4259-bd2f-bf84cdac5572" />

---

## Part 3: Ubuntu Client Configuration

### 1. Client Network Setup

**DNS Mapping**
Update `/etc/hosts` on the client to resolve the mail server.

```bash
sudo nano /etc/hosts
# Add:
192.168.200.3 bnaserver.bungkus.org
```

<img width="1683" height="742" alt="image" src="https://github.com/user-attachments/assets/34571c35-1f98-4b8f-90d5-e97559f02c22" />

**Connectivity Check**

```bash
ping -c 3 bnaserver.bungkus.org
telnet bnaserver.bungkus.org 25
```

<img width="1499" height="339" alt="image" src="https://github.com/user-attachments/assets/5cd57efe-74b2-45cb-9568-9d3d727cfae1" />

### 2. Client Application Setup

**Install Thunderbird**
Download and install the Thunderbird mail client.

```bash
wget https://download.mozilla.org/?product=thunderbird-latest-ssl&os=linux64&lang=en-US -O thunderbird.tar.bz2
tar -xvf thunderbird*.tar.xz
sudo mv thunderbird /opt/
sudo ln -sf /opt/thunderbird/thunderbird /usr/bin/thunderbird
```

<img width="1334" height="195" alt="image" src="https://github.com/user-attachments/assets/b8bf9cce-a3e4-4222-9cb0-bc8ebd3d24f8" />

### 3. Certificate Distribution

Temporarily expose the certificate via HTTP to secure transfer to the client.

**Server Side:**

```bash
sudo firewall-cmd --add-port=80/tcp
cd /etc/pki/tls/certs/
sudo python3 -m http.server 80
```

<img width="1423" height="113" alt="image" src="https://github.com/user-attachments/assets/e179e6f3-62cc-4077-9b7c-2e58c5595704" />
<img width="1271" height="176" alt="image" src="https://github.com/user-attachments/assets/8bbcd397-be48-4cc8-a6a7-932c287eada3" />

**Client Side:**
Access `http://192.168.200.3/bnaserver.pem` via browser and save the certificate.

<img width="800" height="264" alt="image" src="https://github.com/user-attachments/assets/93db93a7-2124-41b8-bbcb-7e6ba6f6744e" />

### 4. Thunderbird Configuration

**Account Settings**
Configure the account with the following parameters:

* **Incoming:** IMAP, `bnaserver.bungkus.org`, Port 993, SSL/TLS, Normal Password
* **Outgoing:** SMTP, `bnaserver.bungkus.org`, Port 465, SSL/TLS, Normal Password

<img width="973" height="341" alt="image" src="https://github.com/user-attachments/assets/7ba92fd4-e9b9-4f3a-a28e-9c49df315792" />

**Certificate Import & OCSP**
Important: Since self-signed certificates are used, OCSP validation must be disabled to prevent connection errors.

1. **Settings > Advanced:** Disable "Query OCSP responder servers".
2. **Certificate Manager:** Import `bnaserver.pem` into the **Authorities** tab and check trust bits.

<img width="990" height="597" alt="image" src="https://github.com/user-attachments/assets/f1d962c2-f0f1-4fe1-b6fa-77e4fc66a3c1" />

**Final Verification**
Send an email from the client to itself. Verify successful transmission and reception in the Inbox.

<img width="2333" height="426" alt="image" src="https://github.com/user-attachments/assets/76fa8ee6-0c3f-4d84-aa47-6e7a9d33781c" />

---
**Deployment Successful.**

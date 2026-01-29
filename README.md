# 🔒 Postfix & Dovecot Mail Server Lab Documentation

> **Complete walkthrough of setting up a secure mail server on Rocky Linux with SSL/TLS encryption and Thunderbird client configuration**

[![Lab Status](https://img.shields.io/badge/Status-Complete-success?style=for-the-badge)](.)
[![Documentation](https://img.shields.io/badge/Documentation-Comprehensive-blue?style=for-the-badge)](./index.html)

## 📋 Overview

This repository contains **complete, exhaustive documentation** of a mail server configuration lab, including:

- ✅ **Postfix SMTP** server setup with SSL/TLS
- ✅ **Dovecot IMAP** server configuration
- ✅ **Self-signed SSL certificates** for secure communication
- ✅ **Thunderbird** client setup and troubleshooting
- ✅ **Every problem encountered** with detailed solutions
- ✅ **75+ screenshots** documenting the entire process

## 🎯 Lab Environment

| Component | Details |
|-----------|---------|
| **Server OS** | Rocky Linux 9 (192.168.200.3) |
| **Client OS** | Ubuntu (192.168.200.80) |
| **Domain** | bungkus.org |
| **FQDN** | bnaserver.bungkus.org |
| **SMTP Server** | Postfix 3.x |
| **IMAP Server** | Dovecot 2.3.16 |
| **Mail Client** | Mozilla Thunderbird 147.0 |
| **Security** | SSL/TLS (Self-signed certificate) |
| **Network** | VirtualBox NAT Network |

## 📖 View the Documentation

**[➡️ Open Complete Documentation (HTML)](./index.html)**

The HTML documentation includes:

- 10 detailed phases from initial setup to final success
- Comprehensive troubleshooting journey
- All configuration files and commands
- Network connectivity crisis resolution
- Certificate authentication challenges
- Complete command reference
- Key lessons learned

## 🚨 Major Challenges Solved

1. **Network Connectivity Loss** - After hostname change, default gateway was removed
2. **OCSP Certificate Hang** - Self-signed certificates causing infinite validation loops
3. **Thunderbird Authentication Issues** - Username format and SSL/TLS configuration
4. **Certificate Import Struggles** - Manual certificate authority setup
5. **"Checking Password" Infinite Loop** - OCSP and certificate validation problems

## 🛠️ Technologies Used

- **Rocky Linux 9** - Enterprise Linux distribution
- **Postfix** - Mail Transfer Agent (MTA)
- **Dovecot** - IMAP/POP3 Server
- **OpenSSL** - SSL/TLS cryptography
- **Mozilla Thunderbird** - Email client
- **VirtualBox** - Virtualization platform

## 📸 Screenshots

All 75 screenshots documenting every step, problem, and solution are included in the `/images` directory and embedded throughout the HTML documentation.

## 🎓 Key Learnings

- Hostname changes can reset network configuration (gateway removal)
- OCSP validation must be disabled for self-signed certificates
- Use system username (not email address) for mail server authentication
- ICMP ping failures don't always indicate network connectivity issues
- Always test locally on the server before troubleshooting remote clients
- Layer-by-layer verification: network → ports → encryption → authentication

## 📊 Lab Statistics

- **Duration**: ~4 hours
- **Major Problems**: 5 critical issues
- **Screenshots**: 75+ images
- **Configuration Files**: 5 modified
- **Ports Configured**: 5 (SMTP: 25, 465, 587 | IMAP: 143, 993)
- **Final Status**: ✅ **FULLY OPERATIONAL**

## ✅ Final Configuration

### Server (Rocky Linux)

```bash
# Services
Postfix (SMTP/SMTPS/Submission)
Dovecot (IMAP/IMAPS)

# Ports
25 (SMTP), 465 (SMTPS), 587 (Submission)
143 (IMAP), 993 (IMAPS)

# SSL/TLS
Self-signed certificate (365 days)
CN: bnaserver.bungkus.org
```

### Client (Ubuntu)

```bash
# Thunderbird Configuration
Incoming: IMAP Port 993 (SSL/TLS)
Outgoing: SMTP Port 465 (SSL/TLS)
Username: nesh
Authentication: Normal Password
OCSP: Disabled
```

## 🚀 Quick Start Commands

### Server Setup

```bash
# Install services
sudo dnf install postfix dovecot -y

# Generate SSL certificate
sudo openssl req -new -x509 -days 365 -nodes \
  -out /etc/pki/tls/certs/bnaserver.pem \
  -keyout /etc/pki/tls/private/bnaserver.key \
  -subj "/C=MY/ST=KL/L=APU/O=SNA/CN=bnaserver.bungkus.org"

# Configure firewall
sudo firewall-cmd --permanent --add-service={smtp,smtps,submission,imap,imaps}
sudo firewall-cmd --reload

# Start services
sudo systemctl start postfix dovecot
sudo systemctl enable postfix dovecot
```

### Client Setup

```bash
# Add server to hosts
echo "192.168.200.3 bnaserver.bungkus.org" | sudo tee -a /etc/hosts

# Install Thunderbird (manual)
cd ~/Downloads
tar -xvf thunderbird-*.tar.xz
sudo mv thunderbird /opt/
sudo ln -sf /opt/thunderbird/thunderbird /usr/bin/thunderbird
```

## 📝 License

This documentation is created for educational purposes as part of a networking and system administration lab.

## 👤 Author

Created as part of Advanced Server Management coursework

---

**⭐ Star this repo if you found it helpful!**

*Last Updated: January 29, 2026*

# 🎓 Complete Beginner's Guide to GitHub Upload

## Step-by-Step with Every Click Explained

> **Don't worry if you've never used GitHub before! This guide assumes ZERO prior knowledge.**

---

## 🎯 What We're Going to Do

1. Create a FREE GitHub account (if you don't have one)
2. Create a new repository on GitHub's website
3. Connect your local folder to GitHub
4. Upload all your files (documentation + 75 images)
5. Make it live as a website (optional)

**Time needed:** 10-15 minutes max

---

## PART 1: Create/Login to GitHub Account

### If You DON'T Have a GitHub Account

1. Go to **<https://github.com>** in your browser
2. Click the big green **"Sign up"** button (top right)
3. Enter:
   - **Email address** (use your real email)
   - **Password** (make it strong)
   - **Username** (this will be in your URL, choose wisely!)
   - Solve the puzzle
4. Click **"Create account"**
5. Check your email and verify
6. You're done! You now have a GitHub account ✅

### If You ALREADY Have a GitHub Account

1. Go to **<https://github.com>**
2. Click **"Sign in"** (top right)
3. Enter your username/email and password
4. You're in! ✅

---

## PART 2: Create a New Repository (Your Project Home)

> **What's a repository?** Think of it like a project folder that lives online forever.

### Step-by-Step

1. **After logging in to GitHub**, you'll see your dashboard

2. **Click the green "New" button** OR click the **"+"** icon in the top-right corner → **"New repository"**

3. **Fill in the form:**

   **Repository name:** (this becomes part of your URL)

   ```
   MailServer-Lab-Documentation
   ```

   ✅ Good names: Use hyphens, no spaces
   ❌ Bad names: "my repo", "Project 1"

   **Description:** (helps people understand what this is)

   ```
   Complete Postfix & Dovecot mail server setup with SSL/TLS - Full troubleshooting documentation with 75 screenshots
   ```

   **Public or Private?**
   - ✅ **Public** = Anyone can see it (good for portfolio!)
   - **Private** = Only you (and people you invite) can see it

   For a lab/portfolio piece, choose **Public**

   **Initialize repository:**
   - ❌ **DO NOT CHECK** "Add a README file" (we already have one!)
   - ❌ **DO NOT CHECK** "Add .gitignore" (we already have one!)
   - ❌ **DO NOT CHECK** "Choose a license" (optional, can do later)

4. **Click the big green "Create repository" button** at the bottom

5. **You'll see a new page with instructions** - Don't panic! We'll use the "push an existing repository" section

6. **IMPORTANT: Copy the repository URL**

   It looks like this:

   ```
   https://github.com/YOUR_USERNAME/MailServer-Lab-Documentation.git
   ```

   There's usually a button to copy it. **Keep this URL handy** - we'll need it in a moment!

---

## PART 3: Set Up Git on Your Computer (One-Time Setup)

> **What's Git?** It's the tool that uploads your files to GitHub. It's probably already on your computer, but let's configure it with your name.

### Open PowerShell

1. Press **Windows key**
2. Type **"PowerShell"**
3. Click **"Windows PowerShell"** (the blue icon)

### Configure Git with Your Identity

Copy and paste these commands **ONE AT A TIME**, replacing with YOUR info:

```powershell
# Set your name (this will show on your commits)
git config --global user.name "Your Actual Name"
```

Press **Enter**

```powershell
# Set your email (use the SAME email as your GitHub account)
git config --global user.email "your.email@example.com"
```

Press **Enter**

**Example:**

```powershell
git config --global user.name "Dineesh Mahendran"
git config --global user.email "dineesh@example.com"
```

✅ **You only have to do this ONCE ever!** Git will remember.

---

## PART 4: Navigate to Your Project Folder

In the same PowerShell window:

```powershell
cd "C:\Users\dinee\Downloads\APU\SNA\MailServer_Lab_Documentation"
```

Press **Enter**

You should see the path change to show you're now in that folder.

**To verify you're in the right place:**

```powershell
dir
```

You should see:

- README.md
- index.html
- images (folder)
- .gitignore

If you see these, you're good! ✅

---

## PART 5: Make Your First Commit (Save Point)

> **What's a commit?** Think of it like saving a version of your project with a description of what you did.

### Run this command

```powershell
git add .
```

Press **Enter**

*This tells Git: "I want to include ALL files in the commit"*

### Now create the commit

```powershell
git commit -m "Initial commit: Complete mail server lab documentation with 75 screenshots"
```

Press **Enter**

You should see output showing all the files being committed. ✅

---

## PART 6: Connect Your Folder to GitHub

> **Now we're telling your local folder:** "Hey, when I say 'upload', send everything to THIS GitHub repository"

### Add the remote (connection to GitHub)

```powershell
git remote add origin YOUR_REPOSITORY_URL_HERE
```

**IMPORTANT:** Replace `YOUR_REPOSITORY_URL_HERE` with the URL you copied from GitHub in Part 2!

**Example:**

```powershell
git remote add origin https://github.com/dineeshmahendran/MailServer-Lab-Documentation.git
```

Press **Enter**

**Verify it worked:**

```powershell
git remote -v
```

You should see your repository URL listed twice (for fetch and push). ✅

---

## PART 7: Upload to GitHub! 🚀

> **This is the moment!** We're sending all 75 images and the documentation to GitHub.

### Push your files

```powershell
git push -u origin master
```

Press **Enter**

### 🔐 Authentication Required

GitHub will ask you to login. **IMPORTANT:**

#### If it opens a browser window

1. It might open Microsoft/GitHub login
2. Sign in with your GitHub account
3. Authorize the application
4. Go back to PowerShell - it should start uploading!

#### If it asks for username/password in the terminal

- **Username:** Your GitHub username
- **Password:** ⚠️ **NOT your GitHub password!** You need a **Personal Access Token**

---

## PART 7B: Creating a Personal Access Token (If Needed)

> **Why?** GitHub stopped accepting passwords in 2021. You need a special token instead.

### Steps to Create Token

1. Go to **<https://github.com>** (in browser)
2. Click your **profile picture** (top right)
3. Click **"Settings"**
4. Scroll down in the left sidebar → Click **"Developer settings"** (very bottom)
5. Click **"Personal access tokens"** → **"Tokens (classic)"**
6. Click **"Generate new token"** → **"Generate new token (classic)"**
7. Fill in:
   - **Note:** `MailServer Lab Upload` (just a reminder for yourself)
   - **Expiration:** `90 days` (or longer)
   - **Scopes:** Check the box for **`repo`** (this gives full repo access)
8. Scroll down, click **"Generate token"**
9. **COPY THE TOKEN IMMEDIATELY!** It looks like: `ghp_abc123def456...`

   ⚠️ **You can only see it ONCE!** Save it somewhere safe.

10. Go back to PowerShell
11. When it asks for password, **paste the token** instead

### Now try the push again

```powershell
git push -u origin master
```

**Enter your username, then paste the token as password.**

### Upload Progress

You'll see:

```
Enumerating objects: 78, done.
Counting objects: 100% (78/78), done.
Delta compression using up to 8 threads
Compressing objects: 100% (77/77), done.
Writing objects: 100% (78/78), 12.34 MiB | 2.34 MiB/s, done.
Total 78 (delta 2), reused 0 (delta 0)
```

✅ **When you see "done" and "Branch 'master' set up to track remote branch 'master'"**, you're successful!

---

## PART 8: Verify It Worked! 🎉

### Check on GitHub

1. Go back to your browser
2. Go to **<https://github.com/YOUR_USERNAME/MailServer-Lab-Documentation>**
3. Refresh the page

**You should now see:**

- ✅ Green "Code" button
- ✅ Your README.md displayed beautifully
- ✅ "images" folder with 75 files
- ✅ index.html file
- ✅ Green commit message at the top

**Click on the "images" folder** - you should see all 75 screenshots!

**🎊 CONGRATULATIONS! Your lab is on GitHub!** 🎊

---

## PART 9: Enable GitHub Pages (Free Website!) 🌐

> **Optional but AWESOME:** Make your HTML documentation viewable as a live website!

### Steps

1. On your repository page, click **"Settings"** (top menu, far right)

2. In the left sidebar, scroll down and click **"Pages"**

3. Under **"Source"**:
   - **Branch:** Select `master` (or `main`)
   - **Folder:** Keep it as `/ (root)`

4. Click **"Save"**

5. **Wait 1-2 minutes** for GitHub to build your site

6. **Refresh the page** - you'll see a green banner with your URL:

   ```
   Your site is live at https://YOUR_USERNAME.github.io/MailServer-Lab-Documentation/
   ```

7. **Click the link** or visit it in a new tab

**🌟 Your documentation is now a LIVE WEBSITE!** 🌟

Anyone with the link can view it beautifully formatted with all 75 screenshots!

---

## 📱 How to Share Your Work

### Share the Repository

```
https://github.com/YOUR_USERNAME/MailServer-Lab-Documentation
```

### Share the Live Website (if you enabled Pages)

```
https://YOUR_USERNAME.github.io/MailServer-Lab-Documentation/
```

**Add to:**

- LinkedIn (Projects section)
- Resume/CV
- Email signature
- Portfolio website

---

## 🔄 Making Updates Later

If you want to update your documentation:

1. **Make changes** to files in:
   `C:\Users\dinee\Downloads\APU\SNA\MailServer_Lab_Documentation`

2. **Open PowerShell** and navigate to the folder:

   ```powershell
   cd "C:\Users\dinee\Downloads\APU\SNA\MailServer_Lab_Documentation"
   ```

3. **Save and upload changes:**

   ```powershell
   git add .
   git commit -m "Updated documentation"
   git push
   ```

Done! Changes appear on GitHub immediately. ✅

---

## ❓ Common Problems & Solutions

### Problem: "fatal: not a git repository"

**Solution:** You're in the wrong folder. Run:

```powershell
cd "C:\Users\dinee\Downloads\APU\SNA\MailServer_Lab_Documentation"
```

### Problem: "error: failed to push some refs"

**Solution:** Someone else made changes (or you edited on GitHub). Run:

```powershell
git pull origin master
git push
```

### Problem: "Permission denied"

**Solution:** Your token expired or username is wrong. Create a new token (Part 7B).

### Problem: Images not showing on GitHub Pages

**Solution:** They should work automatically with relative paths. Wait 5 minutes after pushing, then hard refresh (Ctrl+F5).

### Problem: "Support for password authentication was removed"

**Solution:** You're using your GitHub password. You MUST use a Personal Access Token (Part 7B).

---

## 🎯 Quick Reference - All Commands

```powershell
# One-time setup
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Navigate to folder
cd "C:\Users\dinee\Downloads\APU\SNA\MailServer_Lab_Documentation"

# Initial upload
git add .
git commit -m "Initial commit: Complete mail server lab documentation"
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin master

# Future updates
git add .
git commit -m "Description of changes"
git push
```

---

## ✨ You're Done

Your comprehensive mail server lab documentation is now:

- ✅ Safely stored on GitHub forever
- ✅ Version controlled (never lose your work)
- ✅ Shareable with a simple link
- ✅ Optionally hosted as a live website
- ✅ Ready to impress on your portfolio!

**Congratulations on completing this lab AND documenting it like a pro!** 🏆

---

*Questions? Stuck? Need help? Just ask!*

**Created:** January 29, 2026  
**Your project:** C:\Users\dinee\Downloads\APU\SNA\MailServer_Lab_Documentation

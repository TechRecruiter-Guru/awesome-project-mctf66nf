# Quick Start Guide - SafetyCase.AI

Get your SafetyCase.AI application running in 5 minutes!

## Prerequisites

- Node.js 18+ installed
- Anthropic API key ([Sign up here](https://console.anthropic.com/))

## Quick Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Create `.env.local` file:

```bash
cp .env.local.example .env.local
```

Edit `.env.local` and add your Anthropic API key:

```env
ANTHROPIC_API_KEY=sk-ant-your-actual-api-key-here
NEXT_PUBLIC_ADMIN_PASSWORD=Muses480!
```

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) 🎉

## Test the Application

### Customer Flow

1. **Landing Page** - Go to http://localhost:3000
2. **Select Template** - Click on any robot type
3. **View Payment Instructions** - Note your Order ID
4. **Access Admin** - Go to http://localhost:3000/admin
5. **Login** - Use password: `Muses480!`
6. **Generate Code** - Click "Generate Code" for your order
7. **Enter Code** - Go to http://localhost:3000/upload
8. **Upload PDF** - Upload a sample PDF (create a test PDF with safety data)
9. **Preview** - Edit the extracted data
10. **Download** - Get your HTML file!

### Admin Flow

1. Go to http://localhost:3000/admin
2. Password: `Muses480!`
3. View all orders
4. Generate confirmation codes for paid orders
5. Track order progress

## Build for Production

```bash
npm run build
npm start
```

## Deploy to Vercel

1. Push to GitHub
2. Import project in Vercel
3. Add environment variables:
   - `ANTHROPIC_API_KEY`
   - `NEXT_PUBLIC_ADMIN_PASSWORD`
4. Deploy!

## Common Issues

### Build Fails
- Make sure all dependencies are installed: `npm install`
- Check Node.js version: `node --version` (should be 18+)

### PDF Upload Fails
- Verify your Anthropic API key is correct
- Check that PDF contains text (not just scanned images)

### Confirmation Code Invalid
- Make sure code is in format: UNLOCK-XXX
- Check that code was generated in admin dashboard
- Verify code hasn't been used already

## Need Help?

- Check the full [README.md](./README.md)
- Review error messages in browser console
- Verify environment variables are set correctly

---

**Pro Tip**: Use the admin dashboard to manually test the entire workflow before deploying to production!

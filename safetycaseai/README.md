# SafetyCase.AI

Automated safety case website creation for Physical AI companies. Generate professional, self-contained safety case websites in minutes using AI-powered data extraction.

## Features

- **5 Industry-Specific Templates**: Humanoid Robots, AMRs, Cobots, Drones, Inspection Robots
- **AI-Powered Extraction**: Automatically extract safety data from PDF documents using Claude API
- **Zero External Dependencies**: No databases, payment processors, or email services required
- **Self-Contained Output**: Download complete HTML files with no external dependencies
- **Admin Dashboard**: Manage orders and generate confirmation codes
- **Manual Payment Flow**: Simple PayPal/Venmo payment instructions

## Tech Stack

- **Next.js 14** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Anthropic Claude API** for PDF data extraction
- **File-based storage** (JSON files)
- **Vercel** deployment ready

## Prerequisites

- Node.js 18+ and npm
- Anthropic API key ([Get one here](https://console.anthropic.com/))

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/safetycaseai.git
   cd safetycaseai
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**

   Create a `.env.local` file in the root directory:
   ```bash
   cp .env.local.example .env.local
   ```

   Edit `.env.local` and add your keys:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   NEXT_PUBLIC_ADMIN_PASSWORD=Muses480!
   ```

4. **Run the development server**
   ```bash
   npm run dev
   ```

   Open [http://localhost:3000](http://localhost:3000) to see the application.

## Project Structure

```
safetycaseai/
├── app/
│   ├── api/                    # API routes
│   │   ├── create-order/       # Order creation
│   │   ├── verify-code/        # Code verification
│   │   ├── extract-pdf/        # PDF extraction with Claude
│   │   ├── populate-template/  # Template population
│   │   ├── download/           # HTML download
│   │   └── admin/              # Admin endpoints
│   ├── order/[templateId]/     # Order page
│   ├── upload/                 # PDF upload page
│   ├── preview/                # Preview & edit page
│   ├── admin/                  # Admin dashboard
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Landing page
│   └── globals.css             # Global styles
├── components/
│   ├── TemplateCard.tsx        # Template selection card
│   ├── PaymentInstructions.tsx # Payment display
│   ├── ConfirmationCodeInput.tsx # Code entry
│   ├── PDFUploader.tsx         # PDF upload component
│   └── PreviewEditor.tsx       # Preview & edit interface
├── lib/
│   ├── types.ts                # TypeScript types
│   ├── claude.ts               # Claude API integration
│   ├── orderManager.ts         # Order CRUD operations
│   ├── codeGenerator.ts        # Confirmation code management
│   └── templateParser.ts       # HTML template parser
├── templates/
│   ├── humanoid.html           # Humanoid robot template
│   ├── amr.html                # AMR template
│   ├── cobot.html              # Cobot template
│   ├── drone.html              # Drone template
│   └── inspection.html         # Inspection robot template
├── data/
│   ├── orders.json             # Orders database
│   └── confirmationCodes.json  # Codes database
└── public/                     # Static assets
```

## Usage Workflow

### For Customers

1. **Select Template**: Choose from 5 robot types on the landing page
2. **Create Order**: Receive a unique Order ID with payment instructions
3. **Make Payment**: Send $2,000 via PayPal or Venmo with Order ID
4. **Receive Code**: Get confirmation code via email after payment verification
5. **Upload PDF**: Enter confirmation code and upload safety case PDF
6. **Edit & Preview**: Review AI-extracted data and make edits
7. **Download**: Get complete, self-contained HTML website

### For Admins

1. **Login**: Access `/admin` with password (default: `Muses480!`)
2. **View Orders**: See all orders with status tracking
3. **Verify Payment**: Manually verify PayPal/Venmo payment receipts
4. **Generate Code**: Create confirmation code for verified orders
5. **Email Customer**: Send confirmation code to customer

## Admin Dashboard

Access the admin dashboard at `/admin` with the password: `Muses480!`

**Features:**
- View all orders with filtering by status
- Generate confirmation codes for paid orders
- Copy codes to clipboard for easy emailing
- Real-time order statistics
- Search and filter capabilities

## Payment Instructions

When a customer creates an order, they receive:

**PayPal Option:**
- Send to: `cgtpa.jp@gmail.com`
- Amount: $2,000 USD
- Note: Order #[ORDER_ID]

**Venmo Option:**
- Send to: `@mastertechnicalrecruiting`
- Amount: $2,000 USD
- Note: Order #[ORDER_ID]

Customers must email receipts to `SafetyCaseAI@physicalAIPros.com` with their Order ID.

## Data Storage

This application uses file-based JSON storage:

- **orders.json**: Stores all order information
- **confirmationCodes.json**: Stores generated codes

These files are located in the `/data` directory and are committed to git for persistence across deployments.

## Deployment

### Deploy to Vercel

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/safetycaseai.git
   git push -u origin main
   ```

2. **Import to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will auto-detect Next.js

3. **Add Environment Variables**
   In Vercel project settings, add:
   - `ANTHROPIC_API_KEY`: Your Anthropic API key
   - `NEXT_PUBLIC_ADMIN_PASSWORD`: Admin password (default: `Muses480!`)

4. **Deploy**
   - Click "Deploy"
   - Your app will be live in minutes!

### Custom Domain (Optional)

In Vercel project settings:
1. Go to "Domains"
2. Add your domain (e.g., `safetycaseai.com`)
3. Follow DNS configuration instructions

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Anthropic Claude API key for PDF extraction | Yes |
| `NEXT_PUBLIC_ADMIN_PASSWORD` | Admin dashboard password | Yes |

## API Endpoints

### Public Endpoints

- `POST /api/create-order` - Create new order
- `POST /api/verify-code` - Verify confirmation code
- `POST /api/extract-pdf` - Extract data from PDF using Claude
- `POST /api/populate-template` - Populate template with data
- `POST /api/download` - Download final HTML file

### Admin Endpoints

- `POST /api/admin/login` - Admin authentication
- `GET /api/admin/get-orders` - Fetch all orders
- `POST /api/admin/activate-order` - Generate confirmation code

## Security Considerations

- Admin password stored in environment variable
- Confirmation codes are single-use
- PDFs deleted after processing
- No sensitive data in client-side code
- Rate limiting recommended for production

## Development

### Build for production
```bash
npm run build
```

### Start production server
```bash
npm start
```

### Linting
```bash
npm run lint
```

## Troubleshooting

### PDF Extraction Fails
- Ensure PDF contains readable text (not scanned images)
- Check Anthropic API key is valid
- Verify API quota/rate limits

### Confirmation Code Not Working
- Check code format: `UNLOCK-XXX`
- Verify code hasn't been used already
- Ensure order status is `code_generated`

### Template Not Populating
- Verify all required data fields are present
- Check template file exists in `/templates`
- Review browser console for errors

## License

MIT License - See LICENSE file for details

## Support

For questions or issues:
- Email: SafetyCaseAI@physicalAIPros.com
- GitHub Issues: [Create an issue](https://github.com/yourusername/safetycaseai/issues)

## Roadmap

- [ ] Email automation integration
- [ ] Stripe payment processing
- [ ] Multi-language support
- [ ] Additional robot templates
- [ ] PDF generation from templates
- [ ] Bulk order management

---

Built with ❤️ using Next.js 14 and Claude AI

import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SafetyCase.AI - Automated Safety Case Websites for Physical AI",
  description: "Professional safety case website generation for robotics and physical AI companies. Choose from 5 industry-specific templates.",
  keywords: ["safety case", "robotics", "AI", "compliance", "automation"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="font-sans">
        <nav className="bg-white border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center">
                <a href="/" className="text-2xl font-bold text-primary-600">
                  SafetyCaseAI
                </a>
              </div>
              <div className="flex items-center space-x-4">
                <a href="/" className="text-gray-600 hover:text-gray-900">
                  Home
                </a>
                <a href="/upload" className="text-gray-600 hover:text-gray-900">
                  Upload
                </a>
                <a href="/admin" className="text-gray-600 hover:text-gray-900">
                  Admin
                </a>
              </div>
            </div>
          </div>
        </nav>
        <main>{children}</main>
        <footer className="bg-gray-800 text-white mt-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="text-center">
              <p className="text-sm">
                &copy; {new Date().getFullYear()} SafetyCaseAI. All rights reserved.
              </p>
              <p className="text-sm mt-2">
                Contact: <a href="mailto:contact@safetycaseai.com" className="text-primary-400 hover:text-primary-300">contact@safetycaseai.com</a>
              </p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}

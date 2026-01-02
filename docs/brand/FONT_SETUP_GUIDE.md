# Phoenix Fonts - Download & Setup Guide

**Purpose**: Acquire and configure Inter, Space Grotesk, and JetBrains Mono fonts  
**Time**: 15-30 minutes  
**Methods**: Google Fonts (CDN), Self-hosted, npm packages

---

## 🎯 Font Stack Overview

```css
--font-display: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
--font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
--font-mono: 'JetBrains Mono', 'Courier New', monospace;
```

**Why These Fonts?**
- **Inter**: Clean, readable, modern (Google uses similar)
- **Space Grotesk**: Geometric, tech-forward (headings)
- **JetBrains Mono**: Developer-friendly, excellent for code

---

## 📦 Method 1: Google Fonts CDN (Fastest)

### Advantages
✅ No downloads required  
✅ Cached across websites  
✅ Auto-updates  
✅ Free forever

### Disadvantages
❌ Requires internet connection  
❌ Third-party dependency  
❌ GDPR concerns (EU)

### Implementation

**Single CDN Link (All Fonts)**:
```html
<!-- Add to <head> of HTML files -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
```

**CSS Usage**:
```css
body {
  font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'Space Grotesk', sans-serif;
}

code, pre {
  font-family: 'JetBrains Mono', monospace;
}
```

**For React/Next.js**:
```tsx
// pages/_document.tsx or app/layout.tsx
import { Html, Head, Main, NextScript } from 'next/document'

export default function Document() {
  return (
    <Html>
      <Head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet" />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}
```

---

## 📦 Method 2: Self-Hosted Fonts (Recommended for Production)

### Advantages
✅ Full control  
✅ No external dependencies  
✅ GDPR compliant  
✅ Faster (no DNS lookup)

### Step 1: Download Font Files

#### Option A: Google Fonts Download Tool

**Using google-webfonts-helper**:
1. Visit: https://gwfh.mranftl.com/fonts
2. Search for each font:
   - Inter
   - Space Grotesk
   - JetBrains Mono
3. Select weights needed:
   - **Inter**: 300, 400, 500, 600, 700
   - **Space Grotesk**: 400, 500, 600, 700
   - **JetBrains Mono**: 400, 500, 600
4. Download .woff2 files (modern browsers)
5. Download .woff files (legacy support)

#### Option B: Direct Download Links

**Inter**:
```bash
# Download Inter font family
curl -L "https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip" -o Inter.zip
unzip Inter.zip -d Inter
```

**Space Grotesk**:
```bash
# Download Space Grotesk
curl -L "https://github.com/floriankarsten/space-grotesk/archive/refs/heads/master.zip" -o SpaceGrotesk.zip
unzip SpaceGrotesk.zip -d SpaceGrotesk
```

**JetBrains Mono**:
```bash
# Download JetBrains Mono
curl -L "https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip" -o JetBrainsMono.zip
unzip JetBrainsMono.zip -d JetBrainsMono
```

### Step 2: Organize Font Files

Create this structure:
```
assets/fonts/
├── Inter/
│   ├── Inter-Light.woff2         (300)
│   ├── Inter-Regular.woff2       (400)
│   ├── Inter-Medium.woff2        (500)
│   ├── Inter-SemiBold.woff2      (600)
│   ├── Inter-Bold.woff2          (700)
│   ├── Inter-Light.woff
│   ├── Inter-Regular.woff
│   ├── Inter-Medium.woff
│   ├── Inter-SemiBold.woff
│   └── Inter-Bold.woff
│
├── SpaceGrotesk/
│   ├── SpaceGrotesk-Regular.woff2    (400)
│   ├── SpaceGrotesk-Medium.woff2     (500)
│   ├── SpaceGrotesk-SemiBold.woff2   (600)
│   ├── SpaceGrotesk-Bold.woff2       (700)
│   ├── SpaceGrotesk-Regular.woff
│   ├── SpaceGrotesk-Medium.woff
│   ├── SpaceGrotesk-SemiBold.woff
│   └── SpaceGrotesk-Bold.woff
│
└── JetBrainsMono/
    ├── JetBrainsMono-Regular.woff2   (400)
    ├── JetBrainsMono-Medium.woff2    (500)
    ├── JetBrainsMono-SemiBold.woff2  (600)
    ├── JetBrainsMono-Regular.woff
    ├── JetBrainsMono-Medium.woff
    └── JetBrainsMono-SemiBold.woff
```

### Step 3: Create @font-face CSS

**File**: `assets/fonts/fonts.css`

```css
/* ============================================
   PHOENIX FONTS - Self-Hosted
   ============================================ */

/* INTER - Body Text */

@font-face {
  font-family: 'Inter';
  src: url('./Inter/Inter-Light.woff2') format('woff2'),
       url('./Inter/Inter-Light.woff') format('woff');
  font-weight: 300;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Inter';
  src: url('./Inter/Inter-Regular.woff2') format('woff2'),
       url('./Inter/Inter-Regular.woff') format('woff');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Inter';
  src: url('./Inter/Inter-Medium.woff2') format('woff2'),
       url('./Inter/Inter-Medium.woff') format('woff');
  font-weight: 500;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Inter';
  src: url('./Inter/Inter-SemiBold.woff2') format('woff2'),
       url('./Inter/Inter-SemiBold.woff') format('woff');
  font-weight: 600;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Inter';
  src: url('./Inter/Inter-Bold.woff2') format('woff2'),
       url('./Inter/Inter-Bold.woff') format('woff');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}

/* SPACE GROTESK - Display/Headings */

@font-face {
  font-family: 'Space Grotesk';
  src: url('./SpaceGrotesk/SpaceGrotesk-Regular.woff2') format('woff2'),
       url('./SpaceGrotesk/SpaceGrotesk-Regular.woff') format('woff');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Space Grotesk';
  src: url('./SpaceGrotesk/SpaceGrotesk-Medium.woff2') format('woff2'),
       url('./SpaceGrotesk/SpaceGrotesk-Medium.woff') format('woff');
  font-weight: 500;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Space Grotesk';
  src: url('./SpaceGrotesk/SpaceGrotesk-SemiBold.woff2') format('woff2'),
       url('./SpaceGrotesk/SpaceGrotesk-SemiBold.woff') format('woff');
  font-weight: 600;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Space Grotesk';
  src: url('./SpaceGrotesk/SpaceGrotesk-Bold.woff2') format('woff2'),
       url('./SpaceGrotesk/SpaceGrotesk-Bold.woff') format('woff');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}

/* JETBRAINS MONO - Code/Monospace */

@font-face {
  font-family: 'JetBrains Mono';
  src: url('./JetBrainsMono/JetBrainsMono-Regular.woff2') format('woff2'),
       url('./JetBrainsMono/JetBrainsMono-Regular.woff') format('woff');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'JetBrains Mono';
  src: url('./JetBrainsMono/JetBrainsMono-Medium.woff2') format('woff2'),
       url('./JetBrainsMono/JetBrainsMono-Medium.woff') format('woff');
  font-weight: 500;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'JetBrains Mono';
  src: url('./JetBrainsMono/JetBrainsMono-SemiBold.woff2') format('woff2'),
       url('./JetBrainsMono/JetBrainsMono-SemiBold.woff') format('woff');
  font-weight: 600;
  font-style: normal;
  font-display: swap;
}

/* ============================================
   FONT STACK DEFINITIONS
   ============================================ */

:root {
  --font-display: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'JetBrains Mono', 'Courier New', 'Consolas', monospace;
}

body {
  font-family: var(--font-body);
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-display);
}

code, pre, kbd, samp {
  font-family: var(--font-mono);
}
```

### Step 4: Import in Your Project

```html
<!-- HTML -->
<link rel="stylesheet" href="/assets/fonts/fonts.css">
```

```css
/* CSS */
@import url('/assets/fonts/fonts.css');
```

```javascript
// JavaScript (Webpack/Vite)
import './assets/fonts/fonts.css';
```

---

## 📦 Method 3: npm Packages (For Node.js Projects)

### Install Packages

```bash
# Install font packages
npm install @fontsource/inter @fontsource/space-grotesk @fontsource/jetbrains-mono
```

### Import in JavaScript/TypeScript

```typescript
// In your main entry file (index.tsx, App.tsx, _app.tsx)

// Inter (body font) - import only weights you need
import '@fontsource/inter/300.css';  // Light
import '@fontsource/inter/400.css';  // Regular
import '@fontsource/inter/500.css';  // Medium
import '@fontsource/inter/600.css';  // SemiBold
import '@fontsource/inter/700.css';  // Bold

// Space Grotesk (display font)
import '@fontsource/space-grotesk/400.css';
import '@fontsource/space-grotesk/500.css';
import '@fontsource/space-grotesk/600.css';
import '@fontsource/space-grotesk/700.css';

// JetBrains Mono (code font)
import '@fontsource/jetbrains-mono/400.css';
import '@fontsource/jetbrains-mono/500.css';
import '@fontsource/jetbrains-mono/600.css';
```

**Or import all weights at once**:
```typescript
import '@fontsource/inter';
import '@fontsource/space-grotesk';
import '@fontsource/jetbrains-mono';
```

### Tailwind CSS Configuration

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Space Grotesk', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Courier New', 'monospace'],
      },
    },
  },
};
```

**Usage in components**:
```tsx
<h1 className="font-display font-bold text-4xl">Phoenix</h1>
<p className="font-sans text-base">Body text here</p>
<code className="font-mono text-sm">const x = 42;</code>
```

---

## 🚀 Automated Setup Script

Save as `setup-fonts.sh`:

```bash
#!/bin/bash

echo "🔤 Setting up Phoenix fonts..."

# Create directory structure
mkdir -p assets/fonts/{Inter,SpaceGrotesk,JetBrainsMono}

# Download Inter
echo "📥 Downloading Inter..."
curl -L "https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip" -o /tmp/Inter.zip
unzip -q /tmp/Inter.zip -d /tmp/Inter
cp /tmp/Inter/Inter\ Desktop/*.otf assets/fonts/Inter/ 2>/dev/null || echo "⚠️  Manual Inter setup required"

# Download Space Grotesk
echo "📥 Downloading Space Grotesk..."
curl -L "https://github.com/floriankarsten/space-grotesk/raw/master/fonts/SpaceGrotesk-Variable.ttf" -o assets/fonts/SpaceGrotesk/SpaceGrotesk-Variable.ttf

# Download JetBrains Mono
echo "📥 Downloading JetBrains Mono..."
curl -L "https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip" -o /tmp/JetBrainsMono.zip
unzip -q /tmp/JetBrainsMono.zip -d /tmp/JetBrainsMono
cp /tmp/JetBrainsMono/fonts/ttf/*.ttf assets/fonts/JetBrainsMono/

# Clean up
rm -rf /tmp/Inter* /tmp/SpaceGrotesk* /tmp/JetBrainsMono*

echo "✅ Fonts downloaded to assets/fonts/"
echo ""
echo "Next steps:"
echo "1. Convert to web fonts (.woff2) using https://transfonter.org"
echo "2. Copy fonts.css from documentation"
echo "3. Import fonts.css in your project"
```

**Run it**:
```bash
chmod +x setup-fonts.sh
./setup-fonts.sh
```

---

## 🔧 Font Conversion (TTF/OTF → WOFF2)

### Online Tool (Easiest)

1. Visit: https://transfonter.org
2. Upload your .ttf or .otf files
3. Settings:
   - ✅ WOFF2 (check)
   - ✅ WOFF (check for older browsers)
   - ✅ Add local() names
   - ✅ Base64 encode (optional, for inline CSS)
4. Click "Convert"
5. Download and extract

### Command Line (Advanced)

**Install fonttools**:
```bash
pip install fonttools brotli
```

**Convert fonts**:
```bash
# Convert TTF to WOFF2
pyftsubset Inter-Regular.ttf \
  --output-file=Inter-Regular.woff2 \
  --flavor=woff2 \
  --layout-features="*" \
  --unicodes="U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
```

---

## 📱 Mobile Apps (React Native)

### For iOS

1. Add fonts to `ios/[ProjectName]/Fonts/` directory
2. Update `Info.plist`:
```xml
<key>UIAppFonts</key>
<array>
  <string>Inter-Regular.ttf</string>
  <string>Inter-Bold.ttf</string>
  <string>SpaceGrotesk-Regular.ttf</string>
  <string>SpaceGrotesk-Bold.ttf</string>
  <string>JetBrainsMono-Regular.ttf</string>
</array>
```

### For Android

1. Create `android/app/src/main/assets/fonts/`
2. Add .ttf files to this directory

### React Native Config

```typescript
// In your styles
const styles = StyleSheet.create({
  heading: {
    fontFamily: 'Space Grotesk',
    fontWeight: '700',
    fontSize: 24,
  },
  body: {
    fontFamily: 'Inter',
    fontWeight: '400',
    fontSize: 16,
  },
  code: {
    fontFamily: 'JetBrains Mono',
    fontWeight: '400',
    fontSize: 14,
  },
});
```

---

## ✅ Verification Checklist

After setup, verify fonts are working:

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="/assets/fonts/fonts.css">
  <style>
    body { font-family: var(--font-body); }
    h1 { font-family: var(--font-display); }
    code { font-family: var(--font-mono); }
  </style>
</head>
<body>
  <h1>Phoenix Network (Space Grotesk)</h1>
  <p>This is body text in Inter font.</p>
  <code>const phoenix = "BDP";</code>
  
  <!-- Check browser DevTools > Network tab -->
  <!-- Look for .woff2 files being loaded -->
</body>
</html>
```

**Browser DevTools Check**:
1. Open Network tab
2. Filter by "Font"
3. Verify .woff2 files load successfully
4. Check sizes (~50-150KB per font is normal)

---

## 🎯 Recommended Approach by Project Type

| Project Type | Method | Reason |
|-------------|--------|--------|
| **Documentation Site** | Google Fonts CDN | Simple, fast, cached |
| **Block Explorer** | Self-hosted | Performance, GDPR |
| **Mobile Wallet** | React Native Assets | Native performance |
| **Mining Pool** | npm packages | Easy updates |
| **Marketing Site** | Self-hosted | Control, speed |
| **Developer Tools** | Google Fonts CDN | Convenience |

---

## 📊 Performance Tips

1. **Subset fonts** (Latin only): Reduces file size 50-70%
2. **Use `font-display: swap`**: Shows fallback font while loading
3. **Preload critical fonts**:
```html
<link rel="preload" href="/fonts/Inter-Regular.woff2" as="font" type="font/woff2" crossorigin>
```
4. **Load variable fonts** (single file, all weights):
```css
@font-face {
  font-family: 'Inter';
  src: url('./Inter-Variable.woff2') format('woff2-variations');
  font-weight: 100 900;
}
```

---

## 🚀 Quick Start Command

**For npm projects**:
```bash
npm install @fontsource/inter @fontsource/space-grotesk @fontsource/jetbrains-mono
```

**For CDN projects**:
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
```

**Done!** 🎉 Your fonts are ready to use.







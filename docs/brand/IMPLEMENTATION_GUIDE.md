# Phoenix Theming - Quick Implementation Guide

**Purpose**: Step-by-step instructions to apply Phoenix branding to each cloned application  
**Time per app**: 2-4 hours  
**Order**: Start with highest visibility applications first

---

## 🎯 Priority Order

1. **Block Explorer** (Blockscout) - Most public-facing
2. **Documentation Site** - Developer entry point
3. **Mobile Wallet** (Rainbow) - User-facing
4. **Mining Pool** - Miner-facing
5. **RPC Gateway UI** - Developer tools

---

## 1️⃣ Block Explorer (Blockscout Fork)

### File Structure
```
blockscout/
├── apps/block_scout_web/
│   ├── assets/
│   │   ├── css/
│   │   │   ├── _variables.scss          ← MODIFY
│   │   │   └── custom-phoenix.scss      ← CREATE
│   │   └── static/
│   │       └── images/
│   │           ├── phoenix-logo.svg     ← ADD
│   │           └── favicon.ico          ← REPLACE
│   └── lib/
│       └── templates/
│           └── layout/
│               └── app.html.eex         ← MODIFY
```

### Step 1: Update Variables

**File**: `apps/block_scout_web/assets/css/_variables.scss`

```scss
// PHOENIX BRAND COLORS
$primary: #FF6B35;           // Phoenix Orange
$secondary: #4A90E2;         // Sky Blue
$tertiary: #FF4500;          // Phoenix Red

// TYPOGRAPHY
$font-family-base: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
$font-family-heading: 'Space Grotesk', sans-serif;
$font-family-monospace: 'JetBrains Mono', 'Courier New', monospace;

// SPACING
$spacer: 1rem;
$border-radius: 0.5rem;
$border-radius-lg: 0.75rem;

// SHADOWS
$box-shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
$box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
$box-shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);

// NAVBAR
$navbar-bg: #FFFFFF;
$navbar-border: 2px solid $primary;
$navbar-height: 64px;
```

### Step 2: Create Custom CSS

**File**: `apps/block_scout_web/assets/css/custom-phoenix.scss` (NEW)

```scss
// Import Google Fonts
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&family=JetBrains+Mono:wght@400;500&display=swap');

// NAVBAR BRANDING
.navbar {
  border-bottom: $navbar-border;
  background: $navbar-bg;
  
  .navbar-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    
    img {
      height: 40px;
      width: auto;
    }
    
    .brand-text {
      font-family: $font-family-heading;
      font-weight: 700;
      font-size: 1.25rem;
      color: #1A1A1A;
      
      .highlight {
        color: $primary;
      }
    }
  }
}

// CARD ACCENTS
.card {
  border-top: 3px solid $primary;
  border-radius: $border-radius-lg;
  
  &:hover {
    box-shadow: $box-shadow-lg;
    transform: translateY(-2px);
    transition: all 0.3s ease;
  }
}

// TRANSACTION STATUS
.transaction-success {
  color: $primary !important;
  font-weight: 600;
}

.badge-success {
  background-color: rgba(255, 107, 53, 0.1);
  color: $primary;
  border: 1px solid $primary;
}

// BUTTONS
.btn-primary {
  background-color: $primary;
  border-color: $primary;
  font-weight: 600;
  
  &:hover {
    background-color: $tertiary;
    border-color: $tertiary;
  }
}

.btn-outline-primary {
  color: $primary;
  border-color: $primary;
  
  &:hover {
    background-color: $primary;
    color: white;
  }
}

// LINKS
a {
  color: $secondary;
  
  &:hover {
    color: $primary;
    text-decoration: none;
  }
}

// TABLES
.table {
  thead {
    background-color: #F5F5F5;
    border-bottom: 2px solid $primary;
    
    th {
      font-weight: 600;
      text-transform: uppercase;
      font-size: 0.875rem;
      letter-spacing: 0.05em;
    }
  }
  
  tbody tr {
    &:hover {
      background-color: rgba(255, 107, 53, 0.05);
    }
  }
}

// ADDRESS/HASH DISPLAY
.address-hash,
.transaction-hash,
.block-hash {
  font-family: $font-family-monospace;
  font-size: 0.875rem;
  color: $secondary;
  
  &:hover {
    color: $primary;
  }
}
```

### Step 3: Update Layout Template

**File**: `apps/block_scout_web/lib/templates/layout/app.html.eex`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
    <title>Phoenix Block Explorer</title>
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="<%= static_path(@conn, "/images/favicon.ico") %>">
    
    <!-- Stylesheets -->
    <link rel="stylesheet" href="<%= static_path(@conn, "/css/app.css") %>">
    <link rel="stylesheet" href="<%= static_path(@conn, "/css/custom-phoenix.css") %>">
  </head>
  
  <body>
    <!-- NAVBAR -->
    <nav class="navbar navbar-expand-lg">
      <div class="container">
        <a class="navbar-brand" href="/">
          <img src="<%= static_path(@conn, "/images/phoenix-logo.svg") %>" alt="Phoenix" />
          <span class="brand-text">
            Phoenix <span class="highlight">Explorer</span>
          </span>
        </a>
        
        <div class="navbar-nav ml-auto">
          <a class="nav-link" href="/blocks">Blocks</a>
          <a class="nav-link" href="/transactions">Transactions</a>
          <a class="nav-link" href="/tokens">Tokens</a>
          <a class="nav-link" href="/apis">API</a>
        </div>
      </div>
    </nav>
    
    <!-- CONTENT -->
    <main class="container mt-4">
      <%= render @view_module, @view_template, assigns %>
    </main>
    
    <!-- FOOTER -->
    <footer class="footer mt-5 py-4 bg-light">
      <div class="container text-center">
        <p class="mb-0">
          Phoenix Block Explorer | 
          <a href="https://docs.bdp.network">Docs</a> | 
          <a href="https://github.com/blockdag-phoenix">GitHub</a>
        </p>
      </div>
    </footer>
    
    <script src="<%= static_path(@conn, "/js/app.js") %>"></script>
  </body>
</html>
```

### Step 4: Add Logo Assets

**Create**: `apps/block_scout_web/assets/static/images/phoenix-logo.svg`

```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
  <!-- Simplified Phoenix Logo - Replace with actual design -->
  
  <!-- DAG Cube (Blue) -->
  <rect x="10" y="20" width="8" height="8" fill="none" stroke="#4A90E2" stroke-width="2"/>
  <rect x="14" y="24" width="8" height="8" fill="none" stroke="#4A90E2" stroke-width="2"/>
  <rect x="18" y="28" width="8" height="8" fill="none" stroke="#4A90E2" stroke-width="2"/>
  
  <!-- Phoenix (Orange) -->
  <path d="M20 5 L25 15 L20 10 L15 15 Z" fill="#FF6B35"/>
  <circle cx="20" cy="8" r="2" fill="#FF4500"/>
</svg>
```

### Step 5: Import Custom CSS

**File**: `apps/block_scout_web/assets/css/app.scss`

Add at the bottom:
```scss
@import "custom-phoenix";
```

### Step 6: Build & Deploy

```bash
cd blockscout
mix deps.get
cd apps/block_scout_web/assets
npm install
npm run deploy
cd ../../..
mix phx.digest
```

---

## 2️⃣ Documentation Site (Docusaurus)

### File Structure
```
docs/
├── docusaurus.config.js      ← MODIFY
├── src/
│   ├── css/
│   │   └── custom.css        ← MODIFY
│   └── components/
│       └── PhoenixLogo.js    ← CREATE
└── static/
    └── img/
        ├── phoenix-logo.svg  ← ADD
        └── favicon.ico       ← REPLACE
```

### Step 1: Update Config

**File**: `docusaurus.config.js`

```javascript
module.exports = {
  title: 'Phoenix Documentation',
  tagline: 'Build on the fastest BlockDAG',
  url: 'https://docs.bdp.network',
  baseUrl: '/',
  favicon: 'img/favicon.ico',
  
  themeConfig: {
    // Color mode
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    
    // Navbar
    navbar: {
      title: 'Phoenix',
      logo: {
        alt: 'Phoenix Logo',
        src: 'img/phoenix-logo.svg',
      },
      items: [
        {
          type: 'doc',
          docId: 'intro',
          position: 'left',
          label: 'Docs',
        },
        {
          to: '/api',
          label: 'API',
          position: 'left',
        },
        {
          href: 'https://github.com/blockdag-phoenix',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    
    // Footer
    footer: {
      style: 'light',
      links: [
        {
          title: 'Docs',
          items: [
            { label: 'Getting Started', to: '/docs/intro' },
            { label: 'API Reference', to: '/api' },
          ],
        },
        {
          title: 'Community',
          items: [
            { label: 'Discord', href: 'https://discord.gg/phoenix' },
            { label: 'Twitter', href: 'https://twitter.com/PhoenixBDP' },
          ],
        },
        {
          title: 'More',
          items: [
            { label: 'GitHub', href: 'https://github.com/blockdag-phoenix' },
            { label: 'Explorer', href: 'https://explorer.bdp.network' },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} BlockDAG Phoenix. Built with Docusaurus.`,
    },
  },
  
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};
```

### Step 2: Custom CSS

**File**: `src/css/custom.css`

```css
/**
 * Phoenix Documentation Theme
 */

/* Import Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ROOT VARIABLES */
:root {
  /* Phoenix Colors */
  --ifm-color-primary: #FF6B35;
  --ifm-color-primary-dark: #FF4500;
  --ifm-color-primary-darker: #E63946;
  --ifm-color-primary-darkest: #C1121F;
  --ifm-color-primary-light: #FF8C42;
  --ifm-color-primary-lighter: #FFA500;
  --ifm-color-primary-lightest: #FFB627;
  
  /* Secondary Colors */
  --ifm-color-secondary: #4A90E2;
  --ifm-color-info: #00D9FF;
  
  /* Typography */
  --ifm-font-family-base: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --ifm-heading-font-family: 'Space Grotesk', var(--ifm-font-family-base);
  --ifm-font-family-monospace: 'JetBrains Mono', 'Courier New', monospace;
  
  /* Spacing */
  --ifm-spacing-horizontal: 1.5rem;
  --ifm-spacing-vertical: 1.5rem;
  --ifm-navbar-height: 4rem;
  
  /* Border Radius */
  --ifm-code-border-radius: 0.5rem;
  --ifm-button-border-radius: 0.5rem;
  --ifm-card-border-radius: 0.75rem;
}

/* DARK MODE */
[data-theme='dark'] {
  --ifm-color-primary: #FF8C42;
  --ifm-background-color: #0A0A0A;
  --ifm-background-surface-color: #1A1A1A;
}

/* NAVBAR */
.navbar {
  border-bottom: 2px solid var(--ifm-color-primary);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.navbar__logo {
  height: 2.5rem;
}

.navbar__title {
  font-family: var(--ifm-heading-font-family);
  font-weight: 700;
  font-size: 1.25rem;
}

/* SIDEBAR */
.menu__link {
  font-weight: 500;
}

.menu__link--active {
  color: var(--ifm-color-primary);
  font-weight: 600;
  border-left: 3px solid var(--ifm-color-primary);
}

/* CODE BLOCKS */
.docusaurus-highlight-code-line {
  background-color: rgba(255, 107, 53, 0.1);
  border-left: 3px solid var(--ifm-color-primary);
  display: block;
  margin: 0 calc(-1 * var(--ifm-pre-padding));
  padding: 0 var(--ifm-pre-padding);
}

/* Inline Code */
code {
  background-color: rgba(255, 107, 53, 0.1);
  color: var(--ifm-color-primary-dark);
  border: 1px solid rgba(255, 107, 53, 0.2);
  border-radius: 0.25rem;
  padding: 0.1rem 0.3rem;
}

/* ADMONITIONS */
.admonition-note {
  border-left-color: var(--ifm-color-primary);
}

.admonition-note .admonition-heading h5 {
  color: var(--ifm-color-primary);
}

/* BUTTONS */
.button--primary {
  background-color: var(--ifm-color-primary);
  border-color: var(--ifm-color-primary);
  font-weight: 600;
}

.button--primary:hover {
  background-color: var(--ifm-color-primary-dark);
  border-color: var(--ifm-color-primary-dark);
}

/* CARDS */
.card {
  border-radius: var(--ifm-card-border-radius);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

/* CUSTOM PHOENIX ELEMENTS */
.phoenix-card {
  border: 2px solid var(--ifm-color-primary);
  border-radius: var(--ifm-card-border-radius);
  padding: 1.5rem;
  margin: 1rem 0;
  background: rgba(255, 107, 53, 0.05);
}

.phoenix-badge {
  display: inline-block;
  background: var(--ifm-color-primary);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* TABLES */
table {
  border-collapse: collapse;
  width: 100%;
}

table thead {
  background: rgba(255, 107, 53, 0.1);
  border-bottom: 2px solid var(--ifm-color-primary);
}

table th {
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
}

table tbody tr:hover {
  background: rgba(255, 107, 53, 0.05);
}
```

### Step 3: Build

```bash
cd docs
npm install
npm run build
npm run serve  # Test locally
```

---

## 3️⃣ Mobile Wallet (Rainbow Fork)

### File Structure
```
rainbow-wallet/
├── src/
│   ├── design-system/
│   │   ├── color/
│   │   │   └── palettes.ts          ← MODIFY
│   │   └── typography.ts            ← MODIFY
│   ├── config/
│   │   └── branding.ts              ← CREATE
│   └── assets/
│       ├── phoenix-logo.png         ← ADD
│       └── phoenix-splash.png       ← ADD
└── app.json                          ← MODIFY
```

### Step 1: Color Palette

**File**: `src/design-system/color/palettes.ts`

```typescript
export const phoenixPalette = {
  // Primary Brand Colors
  phoenixOrange: '#FF6B35',
  phoenixRed: '#FF4500',
  phoenixGold: '#FFA500',
  
  // Secondary Colors
  deepBlue: '#0A1929',
  skyBlue: '#4A90E2',
  electricBlue: '#00D9FF',
  
  // Neutrals
  black: '#000000',
  darkGray: '#1A1A1A',
  mediumGray: '#666666',
  lightGray: '#E5E5E5',
  offWhite: '#F5F5F5',
  white: '#FFFFFF',
  
  // Semantic
  success: '#10B981',
  warning: '#F59E0B',
  error: '#EF4444',
  info: '#3B82F6',
  
  // Alpha variants
  phoenixOrange10: 'rgba(255, 107, 53, 0.1)',
  phoenixOrange20: 'rgba(255, 107, 53, 0.2)',
  phoenixOrange50: 'rgba(255, 107, 53, 0.5)',
};

// Export as default theme
export const defaultPalette = phoenixPalette;
```

### Step 2: Typography

**File**: `src/design-system/typography.ts`

```typescript
export const typography = {
  fontFamily: {
    rounded: 'Inter, system-ui, -apple-system, sans-serif',
    display: 'Space Grotesk, system-ui, -apple-system, sans-serif',
    mono: 'JetBrains Mono, Courier New, monospace',
  },
  
  fontSize: {
    xs: 12,
    sm: 14,
    base: 16,
    lg: 18,
    xl: 20,
    '2xl': 24,
    '3xl': 30,
    '4xl': 36,
  },
  
  fontWeight: {
    light: '300',
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
  },
};
```

### Step 3: Branding Config

**File**: `src/config/branding.ts` (NEW)

```typescript
export const BRANDING = {
  // App Identity
  appName: 'Phoenix Wallet',
  tokenSymbol: 'BDP',
  networkName: 'Phoenix Network',
  
  // Assets
  logoPath: require('../assets/phoenix-logo.png'),
  splashScreen: require('../assets/phoenix-splash.png'),
  iconPath: require('../assets/phoenix-icon.png'),
  
  // Network Config
  chainId: 10101,
  rpcUrl: 'https://rpc.bdp.network',
  explorerUrl: 'https://explorer.bdp.network',
  
  // Links
  websiteUrl: 'https://bdp.network',
  docsUrl: 'https://docs.bdp.network',
  githubUrl: 'https://github.com/blockdag-phoenix',
  discordUrl: 'https://discord.gg/phoenix',
  twitterUrl: 'https://twitter.com/PhoenixBDP',
};
```

### Step 4: App Configuration

**File**: `app.json`

```json
{
  "expo": {
    "name": "Phoenix Wallet",
    "slug": "phoenix-wallet",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./src/assets/phoenix-icon.png",
    "splash": {
      "image": "./src/assets/phoenix-splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#FFFFFF"
    },
    "primaryColor": "#FF6B35",
    "androidStatusBar": {
      "backgroundColor": "#FF6B35"
    },
    "ios": {
      "bundleIdentifier": "network.phoenix.wallet",
      "supportsTablet": true
    },
    "android": {
      "package": "network.phoenix.wallet",
      "adaptiveIcon": {
        "foregroundImage": "./src/assets/phoenix-icon.png",
        "backgroundColor": "#FFFFFF"
      }
    }
  }
}
```

---

## 🚀 Quick Start Script

Save this as `apply-phoenix-theme.sh`:

```bash
#!/bin/bash

echo "🔥 Applying Phoenix Theme..."

APP_TYPE=$1

case $APP_TYPE in
  "explorer")
    echo "Theming Block Explorer (Blockscout)..."
    # Add logo
    cp assets/brand/phoenix-logo.svg blockscout/apps/block_scout_web/assets/static/images/
    # Apply theme (manual steps required)
    echo "✅ Logo added. Follow manual steps in THEMING_SYSTEM.md"
    ;;
    
  "docs")
    echo "Theming Documentation Site..."
    cp assets/brand/phoenix-logo.svg docs/static/img/
    cp assets/brand/favicon.ico docs/static/img/
    echo "✅ Assets added. Run: cd docs && npm run build"
    ;;
    
  "wallet")
    echo "Theming Mobile Wallet..."
    cp assets/brand/phoenix-logo.png rainbow-wallet/src/assets/
    echo "✅ Assets added. Update config files manually."
    ;;
    
  *)
    echo "Usage: ./apply-phoenix-theme.sh [explorer|docs|wallet]"
    exit 1
    ;;
esac

echo "🎨 Theme application complete!"
```

**Usage**:
```bash
chmod +x apply-phoenix-theme.sh
./apply-phoenix-theme.sh explorer
```

---

## ✅ Testing Checklist

After theming each application:

1. **Visual Check**:
   - [ ] Logo displays correctly
   - [ ] Colors match Phoenix palette
   - [ ] Fonts are Inter/Space Grotesk

2. **Functionality**:
   - [ ] All pages load
   - [ ] Navigation works
   - [ ] Forms submit correctly

3. **Responsive**:
   - [ ] Mobile view (375px)
   - [ ] Tablet view (768px)
   - [ ] Desktop view (1440px)

4. **Dark Mode** (if applicable):
   - [ ] Colors adjust properly
   - [ ] Contrast is sufficient
   - [ ] Logo variant switches

5. **Performance**:
   - [ ] Page load < 3s
   - [ ] No console errors
   - [ ] Fonts load properly

---

**Next**: Pick your first app and start theming! Block Explorer is recommended as it's the most visible.







# BlockDAG Phoenix - Universal Theming System

**Status**: Brand Implementation Guide  
**Purpose**: Consistent visual identity across all cloned/forked applications  
**Applies To**: Explorer, Wallet, Pool, RPC Gateway, Documentation, Marketing Site, All SDKs

---

## 🎯 Design System Overview

**Goal**: Every BDP application should be **instantly recognizable** as part of the Phoenix ecosystem.

**Principles**:
1. **Consistency** - Same colors, fonts, spacing everywhere
2. **Simplicity** - Google-level clean interface
3. **Phoenix Identity** - Orange/red accents, cube motifs
4. **Professional** - Trust-building, enterprise-ready

---

## 🎨 Core Brand Tokens

### Color Palette (Master Reference)

```css
/* PRIMARY COLORS */
--phoenix-orange: #FF6B35;      /* Primary brand color */
--phoenix-red: #FF4500;         /* Accent, CTAs, highlights */
--phoenix-gold: #FFA500;        /* Success, positive states */

/* SECONDARY COLORS */
--deep-blue: #0A1929;           /* Headers, dark elements */
--sky-blue: #4A90E2;            /* Links, interactive elements */
--electric-blue: #00D9FF;       /* Highlights, hover states */

/* NEUTRAL COLORS */
--black: #000000;               /* Text, strong contrast */
--dark-gray: #1A1A1A;           /* Body text, secondary text */
--medium-gray: #666666;         /* Tertiary text, disabled */
--light-gray: #E5E5E5;          /* Borders, dividers */
--off-white: #F5F5F5;           /* Backgrounds, cards */
--white: #FFFFFF;               /* Primary background */

/* SEMANTIC COLORS */
--success: #10B981;             /* Success states */
--warning: #F59E0B;             /* Warnings */
--error: #EF4444;               /* Errors, critical alerts */
--info: #3B82F6;                /* Info messages */

/* DARK MODE */
--dark-bg: #0A0A0A;             /* Dark mode background */
--dark-card: #1A1A1A;           /* Dark mode cards */
--dark-text: #F5F5F5;           /* Dark mode text */
--dark-border: #333333;         /* Dark mode borders */
```

---

### Typography System

```css
/* FONT FAMILIES */
--font-display: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
--font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
--font-mono: 'JetBrains Mono', 'Courier New', monospace;

/* FONT SIZES (Responsive Scale) */
--text-xs: 0.75rem;      /* 12px */
--text-sm: 0.875rem;     /* 14px */
--text-base: 1rem;       /* 16px */
--text-lg: 1.125rem;     /* 18px */
--text-xl: 1.25rem;      /* 20px */
--text-2xl: 1.5rem;      /* 24px */
--text-3xl: 1.875rem;    /* 30px */
--text-4xl: 2.25rem;     /* 36px */
--text-5xl: 3rem;        /* 48px */

/* FONT WEIGHTS */
--font-light: 300;
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;

/* LINE HEIGHTS */
--leading-tight: 1.2;
--leading-normal: 1.5;
--leading-relaxed: 1.75;
```

---

### Spacing System (8px Grid)

```css
/* SPACING SCALE */
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
--space-24: 6rem;     /* 96px */

/* COMMON PATTERNS */
--padding-card: var(--space-6);
--padding-section: var(--space-12);
--margin-section: var(--space-16);
--gap-grid: var(--space-6);
```

---

### Border Radius

```css
/* RADIUS SCALE */
--radius-sm: 0.25rem;    /* 4px - small elements */
--radius-md: 0.5rem;     /* 8px - buttons, inputs */
--radius-lg: 0.75rem;    /* 12px - cards */
--radius-xl: 1rem;       /* 16px - large containers */
--radius-full: 9999px;   /* Circular elements */
```

---

### Shadows

```css
/* SHADOW SYSTEM */
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);

/* PHOENIX GLOW (Use sparingly) */
--glow-orange: 0 0 20px rgba(255, 107, 53, 0.3);
--glow-blue: 0 0 20px rgba(74, 144, 226, 0.3);
```

---

## 🎨 Component Theming Guide

### Buttons

```css
/* PRIMARY BUTTON */
.btn-primary {
  background: var(--phoenix-orange);
  color: var(--white);
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-md);
  font-family: var(--font-body);
  font-weight: var(--font-semibold);
  font-size: var(--text-base);
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: var(--phoenix-red);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

/* SECONDARY BUTTON */
.btn-secondary {
  background: transparent;
  color: var(--phoenix-orange);
  border: 2px solid var(--phoenix-orange);
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-md);
  font-family: var(--font-body);
  font-weight: var(--font-semibold);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: var(--phoenix-orange);
  color: var(--white);
}

/* GHOST BUTTON */
.btn-ghost {
  background: transparent;
  color: var(--dark-gray);
  padding: var(--space-3) var(--space-6);
  border: none;
  font-family: var(--font-body);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-ghost:hover {
  background: var(--off-white);
}
```

---

### Cards

```css
/* STANDARD CARD */
.card {
  background: var(--white);
  border-radius: var(--radius-lg);
  padding: var(--padding-card);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--light-gray);
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

/* FEATURE CARD (with icon) */
.card-feature {
  background: var(--white);
  border-radius: var(--radius-lg);
  padding: var(--space-8);
  text-align: center;
  border: 2px solid var(--light-gray);
  transition: all 0.3s ease;
}

.card-feature:hover {
  border-color: var(--phoenix-orange);
  box-shadow: var(--glow-orange);
}

/* DARK MODE CARD */
.card-dark {
  background: var(--dark-card);
  border: 1px solid var(--dark-border);
}
```

---

### Navigation

```css
/* NAVBAR */
.navbar {
  background: var(--white);
  border-bottom: 1px solid var(--light-gray);
  padding: var(--space-4) var(--space-8);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* LOGO */
.navbar-logo {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.navbar-logo img {
  height: 40px;
  width: auto;
}

.navbar-logo-text {
  font-family: var(--font-display);
  font-weight: var(--font-bold);
  font-size: var(--text-xl);
  color: var(--dark-gray);
}

/* NAV LINKS */
.nav-link {
  color: var(--dark-gray);
  text-decoration: none;
  font-family: var(--font-body);
  font-weight: var(--font-medium);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-md);
  transition: all 0.2s ease;
}

.nav-link:hover {
  color: var(--phoenix-orange);
  background: var(--off-white);
}

.nav-link.active {
  color: var(--phoenix-orange);
  font-weight: var(--font-semibold);
}
```

---

### Forms & Inputs

```css
/* INPUT FIELD */
.input {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  font-family: var(--font-body);
  font-size: var(--text-base);
  border: 2px solid var(--light-gray);
  border-radius: var(--radius-md);
  background: var(--white);
  color: var(--dark-gray);
  transition: all 0.2s ease;
}

.input:focus {
  outline: none;
  border-color: var(--phoenix-orange);
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
}

.input::placeholder {
  color: var(--medium-gray);
}

/* LABEL */
.label {
  display: block;
  font-family: var(--font-body);
  font-weight: var(--font-medium);
  font-size: var(--text-sm);
  color: var(--dark-gray);
  margin-bottom: var(--space-2);
}

/* SELECT DROPDOWN */
.select {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  font-family: var(--font-body);
  font-size: var(--text-base);
  border: 2px solid var(--light-gray);
  border-radius: var(--radius-md);
  background: var(--white);
  cursor: pointer;
}
```

---

### Tables

```css
/* TABLE CONTAINER */
.table-container {
  overflow-x: auto;
  border-radius: var(--radius-lg);
  border: 1px solid var(--light-gray);
}

/* TABLE */
.table {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--font-body);
}

/* TABLE HEADER */
.table thead {
  background: var(--off-white);
  border-bottom: 2px solid var(--light-gray);
}

.table th {
  padding: var(--space-4);
  text-align: left;
  font-weight: var(--font-semibold);
  font-size: var(--text-sm);
  color: var(--dark-gray);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* TABLE BODY */
.table tbody tr {
  border-bottom: 1px solid var(--light-gray);
  transition: background 0.2s ease;
}

.table tbody tr:hover {
  background: var(--off-white);
}

.table td {
  padding: var(--space-4);
  font-size: var(--text-sm);
  color: var(--dark-gray);
}

/* MONOSPACE COLUMNS (addresses, hashes) */
.table td.mono {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--sky-blue);
}
```

---

### Badges & Pills

```css
/* BADGE */
.badge {
  display: inline-flex;
  align-items: center;
  padding: var(--space-1) var(--space-3);
  font-family: var(--font-body);
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  border-radius: var(--radius-full);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* BADGE VARIANTS */
.badge-success {
  background: rgba(16, 185, 129, 0.1);
  color: var(--success);
}

.badge-warning {
  background: rgba(245, 158, 11, 0.1);
  color: var(--warning);
}

.badge-error {
  background: rgba(239, 68, 68, 0.1);
  color: var(--error);
}

.badge-info {
  background: rgba(59, 130, 246, 0.1);
  color: var(--info);
}

.badge-phoenix {
  background: rgba(255, 107, 53, 0.1);
  color: var(--phoenix-orange);
}
```

---

### Loading States

```css
/* SPINNER */
.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid var(--light-gray);
  border-top-color: var(--phoenix-orange);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* SKELETON LOADER */
.skeleton {
  background: linear-gradient(
    90deg,
    var(--light-gray) 25%,
    var(--off-white) 50%,
    var(--light-gray) 75%
  );
  background-size: 200% 100%;
  animation: loading 1.5s ease-in-out infinite;
  border-radius: var(--radius-md);
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

---

## 🔧 Application-Specific Theming

### 1. Block Explorer (Blockscout Fork)

**Override Variables**:
```scss
// blockscout/apps/block_scout_web/assets/css/_variables.scss

$primary-color: #FF6B35;        // Phoenix Orange
$secondary-color: #4A90E2;      // Sky Blue
$accent-color: #FF4500;         // Phoenix Red

$font-family-base: 'Inter', sans-serif;
$font-family-heading: 'Space Grotesk', sans-serif;
$font-family-monospace: 'JetBrains Mono', monospace;

$border-radius-base: 0.5rem;
$border-radius-lg: 0.75rem;

// Custom Phoenix Branding
$logo-path: '/images/phoenix-logo.svg';
$favicon-path: '/images/favicon.ico';
```

**Header Customization**:
```html
<!-- blockscout/apps/block_scout_web/lib/templates/layout/app.html.eex -->

<header class="navbar navbar-phoenix">
  <div class="navbar-logo">
    <img src="/images/phoenix-logo.svg" alt="BlockDAG Phoenix" />
    <span class="navbar-logo-text">Phoenix Explorer</span>
  </div>
  <!-- nav links -->
</header>
```

**Custom CSS**:
```css
/* blockscout/apps/block_scout_web/assets/css/custom.css */

.navbar-phoenix {
  background: var(--white);
  border-bottom: 2px solid var(--phoenix-orange);
}

.card-phoenix {
  border-top: 3px solid var(--phoenix-orange);
}

.transaction-success {
  color: var(--phoenix-orange);
}
```

---

### 2. Mobile Wallet (Rainbow Fork)

**Theme Configuration**:
```typescript
// rainbow-wallet/src/design-system/color/palettes.ts

export const phoenixPalette = {
  // Primary
  phoenixOrange: '#FF6B35',
  phoenixRed: '#FF4500',
  phoenixGold: '#FFA500',
  
  // Secondary
  deepBlue: '#0A1929',
  skyBlue: '#4A90E2',
  electricBlue: '#00D9FF',
  
  // Neutrals
  black: '#000000',
  darkGray: '#1A1A1A',
  lightGray: '#E5E5E5',
  white: '#FFFFFF',
};

// rainbow-wallet/src/design-system/typography.ts

export const typography = {
  fontFamily: {
    rounded: 'Inter, system-ui',
    display: 'Space Grotesk, system-ui',
    mono: 'JetBrains Mono, monospace',
  },
};
```

**Branding Assets**:
```typescript
// rainbow-wallet/src/config/branding.ts

export const BRANDING = {
  appName: 'Phoenix Wallet',
  tokenSymbol: 'BDP',
  networkName: 'Phoenix Network',
  logoPath: '@assets/phoenix-logo.png',
  splashScreen: '@assets/phoenix-splash.png',
  iconPath: '@assets/phoenix-icon.png',
};
```

**Navigation Theme**:
```tsx
// rainbow-wallet/src/navigation/Routes.tsx

import { phoenixPalette } from '@/design-system/color/palettes';

const navigationTheme = {
  colors: {
    primary: phoenixPalette.phoenixOrange,
    background: phoenixPalette.white,
    card: phoenixPalette.white,
    text: phoenixPalette.darkGray,
    border: phoenixPalette.lightGray,
  },
};
```

---

### 3. Mining Pool (Open-Ethereum-Pool Fork)

**Configuration**:
```json
// open-ethereum-pool/www/config/environment.js

module.exports = {
  APP: {
    name: 'Phoenix Mining Pool',
    ApiUrl: '//pool-api.bdp.network/',
    
    // Branding
    primaryColor: '#FF6B35',
    accentColor: '#FF4500',
    logo: '/assets/phoenix-pool-logo.svg',
    
    // Network
    blockchain: {
      name: 'Phoenix Network',
      symbol: 'BDP',
      networkId: 10101,
      rpcUrl: 'https://rpc.bdp.network',
    },
  },
};
```

**CSS Overrides**:
```css
/* open-ethereum-pool/www/app/styles/app.css */

:root {
  --primary-color: #FF6B35;
  --accent-color: #FF4500;
  --dark-bg: #0A1929;
}

.navbar-brand {
  color: var(--primary-color) !important;
}

.btn-primary {
  background-color: var(--primary-color) !important;
  border-color: var(--primary-color) !important;
}

.stats-card {
  border-top: 3px solid var(--primary-color);
}
```

---

### 4. Documentation Site (Docusaurus)

**Theme Configuration**:
```javascript
// docs/docusaurus.config.js

module.exports = {
  title: 'Phoenix Documentation',
  tagline: 'Build on the Phoenix Network',
  url: 'https://docs.bdp.network',
  favicon: 'img/favicon.ico',
  
  themeConfig: {
    colorMode: {
      defaultMode: 'light',
      respectPrefersColorScheme: true,
    },
    
    navbar: {
      title: 'Phoenix',
      logo: {
        alt: 'Phoenix Logo',
        src: 'img/phoenix-logo.svg',
      },
      items: [
        { to: 'docs/', label: 'Docs', position: 'left' },
        { to: 'api/', label: 'API', position: 'left' },
        { href: 'https://github.com/blockdag-phoenix', label: 'GitHub', position: 'right' },
      ],
    },
    
    // Custom CSS
    customCss: require.resolve('./src/css/custom.css'),
  },
};
```

**Custom Styles**:
```css
/* docs/src/css/custom.css */

:root {
  /* Phoenix Colors */
  --ifm-color-primary: #FF6B35;
  --ifm-color-primary-dark: #FF4500;
  --ifm-color-primary-light: #FFA500;
  
  /* Typography */
  --ifm-font-family-base: 'Inter', sans-serif;
  --ifm-heading-font-family: 'Space Grotesk', sans-serif;
  --ifm-font-family-monospace: 'JetBrains Mono', monospace;
  
  /* Spacing */
  --ifm-spacing-horizontal: 1.5rem;
  --ifm-navbar-height: 4rem;
}

/* Phoenix Glow Effect on Code Blocks */
.docusaurus-highlight-code-line {
  background-color: rgba(255, 107, 53, 0.1);
  border-left: 3px solid var(--ifm-color-primary);
}

/* Custom Cards */
.phoenix-card {
  border: 2px solid var(--ifm-color-primary);
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin: 1rem 0;
}
```

---

### 5. RPC Gateway UI

**React Theme Provider**:
```typescript
// rpc-gateway-ui/src/theme/phoenixTheme.ts

import { createTheme } from '@mui/material/styles';

export const phoenixTheme = createTheme({
  palette: {
    primary: {
      main: '#FF6B35',
      dark: '#FF4500',
      light: '#FFA500',
    },
    secondary: {
      main: '#4A90E2',
      dark: '#0A1929',
      light: '#00D9FF',
    },
    background: {
      default: '#FFFFFF',
      paper: '#F5F5F5',
    },
    text: {
      primary: '#1A1A1A',
      secondary: '#666666',
    },
  },
  
  typography: {
    fontFamily: '"Inter", "Helvetica", "Arial", sans-serif',
    h1: { fontFamily: '"Space Grotesk", sans-serif' },
    h2: { fontFamily: '"Space Grotesk", sans-serif' },
    h3: { fontFamily: '"Space Grotesk", sans-serif' },
    fontFamilyMonospace: '"JetBrains Mono", monospace',
  },
  
  shape: {
    borderRadius: 8,
  },
  
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },
  },
});
```

---

## 📦 Asset Package

### Required Brand Assets for Each Application

```
/assets/brand/
├── logos/
│   ├── phoenix-logo-full.svg        (full logo with text)
│   ├── phoenix-logo-icon.svg        (icon only)
│   ├── phoenix-logo-horizontal.svg  (horizontal lockup)
│   ├── phoenix-logo-white.svg       (for dark backgrounds)
│   └── phoenix-logo-monochrome.svg  (single color)
│
├── icons/
│   ├── favicon.ico
│   ├── favicon-16.png
│   ├── favicon-32.png
│   ├── favicon-64.png
│   ├── apple-touch-icon.png
│   └── android-chrome-512.png
│
├── backgrounds/
│   ├── hero-background.svg          (geometric pattern)
│   ├── cube-pattern.svg             (DAG cube motif)
│   └── phoenix-gradient.svg         (gradient background)
│
├── illustrations/
│   ├── error-404.svg
│   ├── empty-state.svg
│   └── loading-animation.svg
│
└── fonts/
    ├── Inter/ (Google Fonts)
    ├── SpaceGrotesk/ (Google Fonts)
    └── JetBrainsMono/ (Google Fonts)
```

---

## 🎨 Dark Mode

### Automatic Dark Mode Toggle

```css
/* Implement using CSS variables and prefers-color-scheme */

:root {
  /* Light mode (default) */
  --bg-primary: #FFFFFF;
  --bg-secondary: #F5F5F5;
  --text-primary: #1A1A1A;
  --text-secondary: #666666;
  --border-color: #E5E5E5;
}

@media (prefers-color-scheme: dark) {
  :root {
    /* Dark mode */
    --bg-primary: #0A0A0A;
    --bg-secondary: #1A1A1A;
    --text-primary: #F5F5F5;
    --text-secondary: #999999;
    --border-color: #333333;
  }
  
  /* Adjust Phoenix colors for dark mode */
  --phoenix-orange: #FF8C42;  /* Slightly brighter */
  --phoenix-red: #FF6347;     /* Softer red */
}

/* Use in components */
body {
  background-color: var(--bg-primary);
  color: var(--text-primary);
}
```

---

## 🚀 Implementation Checklist

### For Each Cloned Application:

- [ ] **Step 1: Install Fonts**
  - Add Inter, Space Grotesk, JetBrains Mono to project
  - Update font-family declarations

- [ ] **Step 2: Replace Logo Assets**
  - Swap existing logo with Phoenix logo
  - Update favicon
  - Update social media preview images

- [ ] **Step 3: Update Color Variables**
  - Find primary color variable (usually in `_variables.scss`, `theme.ts`, or `config.js`)
  - Replace with Phoenix Orange (#FF6B35)
  - Replace secondary colors with Phoenix palette

- [ ] **Step 4: Update Typography**
  - Set heading font to Space Grotesk
  - Set body font to Inter
  - Set monospace font to JetBrains Mono

- [ ] **Step 5: Customize Components**
  - Update button styles
  - Update card styles
  - Update navigation/header
  - Update footer

- [ ] **Step 6: Update Text Content**
  - Replace app name with "Phoenix [Type]" (e.g., "Phoenix Explorer")
  - Update token symbol to BDP
  - Update network name to "Phoenix Network"
  - Update URLs/links to bdp.network domains

- [ ] **Step 7: Test Dark Mode**
  - Ensure colors work in both light/dark modes
  - Test contrast ratios (WCAG AA compliance)

- [ ] **Step 8: Browser Testing**
  - Chrome/Safari/Firefox
  - Mobile responsive
  - Cross-browser font rendering

---

## 📝 Code Templates

### CSS Variables Setup

```css
/* Copy this to the root of your main CSS file */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  /* Colors */
  --phoenix-orange: #FF6B35;
  --phoenix-red: #FF4500;
  --phoenix-gold: #FFA500;
  --deep-blue: #0A1929;
  --sky-blue: #4A90E2;
  --electric-blue: #00D9FF;
  --black: #000000;
  --dark-gray: #1A1A1A;
  --medium-gray: #666666;
  --light-gray: #E5E5E5;
  --off-white: #F5F5F5;
  --white: #FFFFFF;
  
  /* Typography */
  --font-display: 'Space Grotesk', sans-serif;
  --font-body: 'Inter', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  
  /* Spacing (8px grid) */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-12: 3rem;
  
  /* Border Radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

* {
  box-sizing: border-box;
}

body {
  font-family: var(--font-body);
  color: var(--dark-gray);
  background: var(--white);
  line-height: 1.6;
  margin: 0;
  padding: 0;
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-display);
  font-weight: 700;
  line-height: 1.2;
}
```

---

### React Theme Provider Template

```typescript
// theme/PhoenixThemeProvider.tsx

import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

const phoenixTheme = createTheme({
  palette: {
    primary: { main: '#FF6B35' },
    secondary: { main: '#4A90E2' },
  },
  typography: {
    fontFamily: '"Inter", sans-serif',
  },
});

export const PhoenixThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <ThemeProvider theme={phoenixTheme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  );
};
```

---

## 🎯 Quality Checklist

Before deploying any themed application:

- [ ] Logo appears correctly on all pages
- [ ] Primary color is Phoenix Orange (#FF6B35)
- [ ] Fonts are Inter (body) and Space Grotesk (headings)
- [ ] All references to old project name are replaced
- [ ] Dark mode works (if implemented)
- [ ] Mobile responsive (test on phone)
- [ ] Loading states use Phoenix colors
- [ ] Error states use Phoenix error color
- [ ] Success states use Phoenix success color
- [ ] Links use Phoenix colors and hover correctly
- [ ] Buttons follow Phoenix button styles
- [ ] Cards have consistent styling
- [ ] Tables are readable and themed
- [ ] Forms have proper focus states (Phoenix orange border)
- [ ] Favicon is Phoenix icon
- [ ] Social media preview image shows Phoenix branding

---

**Next Step**: Pick your first application to theme (recommend starting with Block Explorer or Documentation site) and work through the implementation checklist systematically.







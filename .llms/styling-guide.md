# MonsterUI Styling Guide for HTML

## Overview
This guide explains how to style HTML elements to match MonsterUI's design system using DaisyUI and Tailwind CSS classes. MonsterUI is explicitly incompatible with Pico CSS.

## Required Setup

Add these to your HTML `<head>`:

```html
<link href="https://cdn.jsdelivr.net/npm/daisyui@4.12.22/dist/full.min.css" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
```

## Basic Layout Structure

Basic page structure:

```html
<body class="bg-background text-foreground">
  <main class="container mx-auto px-4">
    <!-- Your content here -->
  </main>
</body>
```

## Common Components

### Cards

```html
<div class="card bg-base-100 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">Card Title</h2>
    <p>Card content goes here</p>
    <div class="card-actions justify-end">
      <button class="btn btn-primary">Action</button>
    </div>
  </div>
</div>
```

### Buttons

```html
<!-- Primary Button -->
<button class="btn btn-primary">Primary Action</button>

<!-- Secondary Button -->
<button class="btn btn-secondary">Secondary Action</button>

<!-- Ghost Button -->
<button class="btn btn-ghost">Ghost Button</button>

<!-- Disabled Button -->
<button class="btn btn-disabled" disabled>Disabled</button>
```

### Forms

```html
<form class="space-y-4">
  <!-- Text Input -->
  <div class="form-control">
    <label class="label">
      <span class="label-text">Username</span>
    </label>
    <input type="text" class="input input-bordered w-full" />
  </div>

  <!-- Select -->
  <div class="form-control">
    <label class="label">
      <span class="label-text">Category</span>
    </label>
    <select class="select select-bordered w-full">
      <option>Option 1</option>
      <option>Option 2</option>
    </select>
  </div>

  <!-- Checkbox -->
  <div class="form-control">
    <label class="label cursor-pointer">
      <span class="label-text">Remember me</span>
      <input type="checkbox" class="checkbox" />
    </label>
  </div>
</form>
```

### Tables

```html
<div class="overflow-x-auto">
  <table class="table table-zebra">
    <thead>
      <tr>
        <th>Name</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Item 1</td>
        <td>Value 1</td>
      </tr>
    </tbody>
  </table>
</div>
```

### Alert Messages

```html
<!-- Success Alert -->
<div class="alert alert-success">
  <span>Operation successful!</span>
</div>

<!-- Error Alert -->
<div class="alert alert-error">
  <span>Something went wrong!</span>
</div>

<!-- Warning Alert -->
<div class="alert alert-warning">
  <span>Proceed with caution!</span>
</div>
```

### Navigation

```html
<nav class="navbar bg-base-100">
  <div class="flex-1">
    <a class="btn btn-ghost text-xl">Brand</a>
  </div>
  <div class="flex-none">
    <ul class="menu menu-horizontal px-1">
      <li><a>Link 1</a></li>
      <li><a>Link 2</a></li>
    </ul>
  </div>
</nav>
```

## Grid Layout

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div class="bg-base-200 p-4">Column 1</div>
  <div class="bg-base-200 p-4">Column 2</div>
  <div class="bg-base-200 p-4">Column 3</div>
</div>
```

## Spacing Classes

- Margin: `m-{size}` (e.g., `m-4`)
- Padding: `p-{size}` (e.g., `p-4`)
- Gap: `gap-{size}` (e.g., `gap-4`)

Sizes range from 0 to 16, representing multiples of 0.25rem.

## Color System

MonsterUI uses themed colors through DaisyUI:

- Primary: `bg-primary text-primary-content`
- Secondary: `bg-secondary text-secondary-content`
- Accent: `bg-accent text-accent-content`
- Neutral: `bg-neutral text-neutral-content`

## Responsive Design

Use breakpoint prefixes:
- `sm:` (640px)
- `md:` (768px)
- `lg:` (1024px)
- `xl:` (1280px)
- `2xl:` (1536px)

Example:
```html
<div class="w-full md:w-1/2 lg:w-1/3">
  Responsive width
</div>
```

## Best Practices

1. Always include both background and text colors for contrast
2. Use semantic HTML elements with appropriate classes
3. Follow mobile-first approach using responsive classes
4. Use container class for consistent page width
5. Implement proper spacing using utility classes

## Theme Support

MonsterUI supports multiple themes. Add the theme class to your HTML tag:

```html
<html class="uk-theme-slate"> <!-- or other theme names -->
```

Available themes:
- slate
- stone
- gray
- neutral
- red
- rose
- orange
- green
- blue
- yellow
- violet
- zinc


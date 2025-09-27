# Testing Your Slayy Extension

## How to Test the Extension

1. **Navigate to the project directory:**
   ```bash
   cd "/Users/mustafax_x/Desktop/hc & j stuff/shopping-ai/shopping-ai"
   ```

2. **Install dependencies (if not already done):**
   ```bash
   pnpm install
   ```

3. **Start the development server:**
   ```bash
   pnpm dev
   ```

4. **Load the extension in Chrome:**
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)
   - Click "Load unpacked"
   - Navigate to the `build/chrome-mv3-dev` folder in your project
   - Select the folder

5. **Test the extension:**
   - Visit any website (like google.com, amazon.com, etc.)
   - You should see the "💅 Slayy" extension appear in the top-right corner
   - The extension will show:
     - Website safety analysis (with loading state)
     - Image upload section
     - AI insights section
   - Click the X button to close the extension

## What the Extension Does

- **Website Safety**: Analyzes the current website and shows if it's safe, caution, or unsafe
- **Image Upload**: Placeholder for uploading images to analyze
- **AI Insights**: Shows personalized advice and recommendations
- **Modern UI**: Clean, modern design with smooth animations
- **Responsive**: Works on any website

## Troubleshooting

If you encounter issues:
1. Make sure you're in the correct directory (`shopping-ai/`)
2. Ensure all dependencies are installed (`pnpm install`)
3. Check that the development server is running (`pnpm dev`)
4. Reload the extension in Chrome if needed
5. Check the browser console for any error messages

The extension should now work perfectly with the new design you requested!

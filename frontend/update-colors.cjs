/**
 * Bulk UI update script
 * Updates all .tsx files with new color fixes, sizing normalization, and responsiveness
 */
const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, 'src');

function getAllTsxFiles(dir) {
    let results = [];
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
            results = results.concat(getAllTsxFiles(fullPath));
        } else if (entry.name.endsWith('.tsx') || entry.name.endsWith('.ts')) {
            results.push(fullPath);
        }
    }
    return results;
}

// Define replacements
const replacements = [
    // ============ KPI CARD FIXES (dark mode remnants) ============
    // Remove dark gradient backgrounds from KPI cards - make them clean light cards
    ['bg-gradient-to-br from-blue-600/20 via-blue-700/10 to-blue-800/20 backdrop-blur-md', 'bg-white'],
    ['bg-gradient-to-br from-purple-600/20 via-purple-700/10 to-purple-800/20 backdrop-blur-md', 'bg-white'],
    ['bg-gradient-to-br from-green-600/20 via-green-700/10 to-green-800/20 backdrop-blur-md', 'bg-white'],
    ['bg-gradient-to-br from-amber-600/20 via-amber-700/10 to-amber-800/20 backdrop-blur-md', 'bg-white'],
    ['bg-gradient-to-br from-cyan-600/20 via-cyan-700/10 to-cyan-800/20 backdrop-blur-md', 'bg-white'],
    ['bg-gradient-to-br from-blue-600/20 to-blue-800/20 backdrop-blur-md', 'bg-white'],
    ['bg-gradient-to-br from-green-600/20 to-green-800/20 backdrop-blur-md', 'bg-white'],
    ['bg-gradient-to-br from-amber-600/20 to-amber-800/20 backdrop-blur-md', 'bg-white'],
    ['bg-gradient-to-br from-purple-600/20 to-purple-800/20 backdrop-blur-md', 'bg-white'],

    // Fix KPI card borders
    ['border-primary-500/30', 'border-primary-200'],
    ['border-primary-500/20', 'border-primary-200'],
    ['border-purple-500/30', 'border-purple-200'],
    ['border-purple-500/20', 'border-purple-200'],
    ['border-green-400/30', 'border-green-200'],
    ['border-green-400/20', 'border-green-200'],
    ['border-amber-500/30', 'border-amber-200'],
    ['border-amber-500/20', 'border-amber-200'],
    ['border-cyan-500/30', 'border-cyan-200'],

    // Fix text colors that are opaque on light bg
    ['text-blue-300/80', 'text-primary-600'],
    ['text-blue-300', 'text-primary-600'],
    ['text-purple-300/80', 'text-purple-600'],
    ['text-purple-300', 'text-purple-600'],
    ['text-green-700/80', 'text-green-600'],
    ['text-amber-300/80', 'text-amber-600'],
    ['text-amber-300', 'text-amber-600'],
    ['text-cyan-300/80', 'text-cyan-600'],
    ['text-cyan-300', 'text-cyan-600'],

    // Fix hover states that won't work on light backgrounds
    ['group-hover:text-blue-100', 'group-hover:text-primary-600'],
    ['group-hover:text-purple-100', 'group-hover:text-purple-600'],
    ['group-hover:text-green-100', 'group-hover:text-green-600'],
    ['group-hover:text-amber-100', 'group-hover:text-amber-600'],
    ['group-hover:text-cyan-100', 'group-hover:text-cyan-600'],

    // Fix hover bg states
    ['hover:border-blue-400/50', 'hover:border-primary-300'],
    ['hover:border-purple-400/50', 'hover:border-purple-300'],
    ['hover:border-green-400/50', 'hover:border-green-300'],
    ['hover:border-amber-400/50', 'hover:border-amber-300'],
    ['hover:border-cyan-400/50', 'hover:border-cyan-300'],

    // ============ CHART SECTION FIXES ============
    ['bg-gradient-to-br from-gray-800/60 via-gray-800/40 to-gray-900/60 backdrop-blur-md', 'bg-white'],

    // ============ SIZE NORMALIZATION ============
    // KPI values - consistent 2xl instead of mixed 3xl/4xl
    ['text-4xl font-bold text-neutral-900 group-hover', 'text-2xl font-bold text-neutral-900 group-hover'],
    ['text-4xl font-bold text-neutral-900\">', 'text-2xl font-bold text-neutral-900\">'],
    ['text-3xl font-bold text-neutral-900 group-hover', 'text-2xl font-bold text-neutral-900 group-hover'],

    // Headers - some pages have text-3xl, normalize to text-2xl
    // (Login excluded as it has its own design)

    // ============ MISC DARK MODE REMNANTS ============
    ['border-dark-600', 'border-light-border'],
    ['border-dark-500', 'border-light-border'],
    ['focus:ring-offset-dark-800', 'focus:ring-offset-white'],
    ['border-gray-800', 'border-light-border'],
    ['divide-gray-700', 'divide-light-border'],
    ['text-primary-400', 'text-primary-500'],

    // ============ BUTTON TEXT ON GRADIENTS ============
    // Gradient buttons should have white text
    ['disabled:cursor-not-allowed text-neutral-900 rounded-lg', 'disabled:cursor-not-allowed text-white rounded-lg'],
];

let totalReplacements = 0;
const files = getAllTsxFiles(srcDir);

for (const filePath of files) {
    let content = fs.readFileSync(filePath, 'utf-8');
    let fileChanged = false;

    for (const [search, replace] of replacements) {
        if (content.includes(search)) {
            const count = content.split(search).length - 1;
            content = content.split(search).join(replace);
            totalReplacements += count;
            fileChanged = true;
            console.log(`  ${path.relative(srcDir, filePath)}: "${search.substring(0, 50)}..." -> "${replace}" (${count}x)`);
        }
    }

    if (fileChanged) {
        fs.writeFileSync(filePath, content, 'utf-8');
    }
}

console.log(`\nDone! Total replacements: ${totalReplacements}`);

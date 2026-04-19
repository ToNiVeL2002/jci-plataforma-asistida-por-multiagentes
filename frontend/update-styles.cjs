const fs = require('fs');
const path = require('path');

const srcPath = path.join(__dirname, 'src');

// Patrones a reemplazar
const replacements = [
    // Fondos oscuros a claros
    { from: /bg-dark-bg/g, to: 'bg-light-bg' },
    { from: /bg-dark-card/g, to: 'bg-light-card' },
    { from: /border-dark-border/g, to: 'border-light-border' },
    { from: /hover:bg-dark-bg/g, to: 'hover:bg-light-hover' },
    { from: /bg-dark-700/g, to: 'bg-neutral-100' },
    { from: /bg-dark-600/g, to: 'bg-neutral-50' },

    // Grises oscuros a claros/blancos
    { from: /bg-gray-900([^/])/g, to: 'bg-light-surface$1' },
    { from: /bg-gray-900\//g, to: 'bg-light-surface/' },
    { from: /bg-gray-800([^/])/g, to: 'bg-white$1' },
    { from: /bg-gray-800\/50/g, to: 'bg-white/80' },
    { from: /bg-gray-800\/30/g, to: 'bg-white/50' },
    { from: /bg-gray-700([^/])/g, to: 'bg-neutral-50$1' },
    { from: /bg-gray-700\//g, to: 'bg-neutral-50/' },
    { from: /bg-gray-600/g, to: 'bg-neutral-200' },

    // Bordes oscuros a claros
    { from: /border-gray-700/g, to: 'border-light-border' },
    { from: /border-gray-600/g, to: 'border-neutral-300' },

    // Texto blanco a oscuro (con cuidado de preservar algunos usos correctos)
    { from: /text-white([^/\-])/g, to: 'text-neutral-900$1' },
    { from: /text-white"/g, to: 'text-neutral-900"' },
    { from: /text-white\s/g, to: 'text-neutral-900 ' },
    { from: /text-gray-400/g, to: 'text-neutral-600' },
    { from: /text-gray-300/g, to: 'text-neutral-700' },

    //Hovers oscuros a claros
    { from: /hover:text-white/g, to: 'hover:text-neutral-900' },
    { from: /hover:bg-gray-800/g, to: 'hover:bg-neutral-100' },
    { from: /hover:bg-gray-700/g, to: 'hover:bg-neutral-50' },
    { from: /hover:bg-gray-600/g, to: 'hover:bg-neutral-200' },

    // Placeholders
    { from: /placeholder-gray-400/g, to: 'placeholder-neutral-400' }
];

function processFile(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;

    replacements.forEach(({ from, to }) => {
        const newContent = content.replace(from, to);
        if (newContent !== content) {
            modified = true;
            content = newContent;
        }
    });

    if (modified) {
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`✓ Updated: ${filePath}`);
        return 1;
    }
    return 0;
}

function processDirectory(dir) {
    let count = 0;
    const items = fs.readdirSync(dir);

    items.forEach(item => {
        const fullPath = path.join(dir, item);
        const stat = fs.statSync(fullPath);

        if (stat.isDirectory()) {
            count += processDirectory(fullPath);
        } else if (fullPath.endsWith('.tsx') || fullPath.endsWith('.ts')) {
            count += processFile(fullPath);
        }
    });

    return count;
}

console.log('Starting style updates...');
const filesModified = processDirectory(srcPath);
console.log(`\n✅ Process complete! Modified ${filesModified} files.`);

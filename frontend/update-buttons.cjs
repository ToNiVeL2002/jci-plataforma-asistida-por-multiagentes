const fs = require('fs');
const path = require('path');

const srcPath = path.join(__dirname, 'src');

// Ajustes finales para colores de botones
const replacements = [
    // Cambiar botones azules a primary (JCI blue)
    { from: /bg-blue-600([^/])/g, to: 'bg-primary-500$1' },
    { from: /bg-blue-600\//g, to: 'bg-primary-500/' },
    { from: /hover:bg-blue-700/g, to: 'hover:bg-primary-600' },
    { from: /bg-blue-500([^/])/g, to: 'bg-primary-500$1' },
    { from: /hover:bg-blue-600/g, to: 'hover:bg-primary-600' },
    { from: /border-blue-500/g, to: 'border-primary-500' },
    { from: /text-blue-400/g, to: 'text-primary-500' },

    // Cambiar botones verdes a secondary (JCI gold) o mantener verde si es éxito
    // Voy a mantener verde para "success" actions pero cambiar el tono
    { from: /bg-green-600([^/])/g, to: 'bg-green-500$1' },
    { from: /hover:bg-green-700/g, to: 'hover:bg-green-600' },
    { from: /border-green-500/g, to: 'border-green-400' },
    { from: /text-green-300/g, to: 'text-green-700' },

    // Botones deben tener texto blanco, no text-neutral-900
    // Buscar patrones específicos de botones
    { from: /(bg-primary-\d+.*?)text-neutral-900/g, to: '$1text-white' },
    { from: /(bg-green-\d+.*?)text-neutral-900/g, to: '$1text-white' },
    { from: /(bg-red-\d+.*?)text-neutral-900/g, to: '$1text-white' },
    { from: /(bg-secondary-\d+.*?)text-neutral-900/g, to: '$1text-neutral-900' }, // Gold buttons keep dark text

    // Corregir iconos SVG en botones que deben ser blancos
    { from: /(w-\d+ h-\d+) text-neutral-900"([^>]*stroke="currentColor")/g, to: '$1 text-white"$2' }
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

console.log('Applying final color adjustments...');
const filesModified = processDirectory(srcPath);
console.log(`\n✅ Final adjustments complete! Modified ${filesModified} files.`);

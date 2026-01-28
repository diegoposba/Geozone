import fs from 'fs';
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.PUBLIC_SUPABASE_URL;
const supabaseKey = process.env.PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
	console.error('Variables d\'environnement manquantes');
	process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

// Mapping des colonnes CSV vers les noms de la base de données
const columnMapping = {
	'Country': 'country',
	'Alcohol': 'alcohol',
	'Army': 'army',
	'Capital City - Numeric': 'capital_city_numeric',
	'Capital City - Ratio': 'capital_city_ratio',
	'Chinese diaspora': 'chinese_diaspora',
	'Low density': 'low_density',
	'EEZ': 'eez',
	'FIFA': 'fifa',
	'Homicide rate': 'homicide_rate',
	'HDI': 'hdi',
	'Individual GDP': 'individual_gdp',
	'Life expectancy': 'life_expectancy',
	'Obesity': 'obesity',
	'Olympics': 'olympics',
	'Superficy (asc)': 'superficy_asc',
	'Median age': 'median_age',
	'Sovereignty': 'sovereignty',
	'Suicide rate': 'suicide_rate',
	'Forest': 'forest'
};

// Lire et parser le CSV
function parseCSV(filePath) {
	const data = fs.readFileSync(filePath, 'utf-8');
	const lines = data.trim().split('\n');
	const headers = lines[0].split(',').map((h) => h.trim());

	const rows = lines.slice(1).map((line, index) => {
		const values = line.split(',').map((v) => v.trim());
		const row = { id: index + 1 }; // ID séquentiel

		headers.forEach((header, colIndex) => {
			const dbColumnName = columnMapping[header];
			if (dbColumnName) {
				const value = isNaN(values[colIndex]) ? values[colIndex] : parseInt(values[colIndex]);
				row[dbColumnName] = value;
			}
		});

		return row;
	});

	return rows;
}

async function uploadData() {
	try {
		console.log('Lecture du CSV...');
		const rows = parseCSV('../Rankings/Data/Rankings.csv');

		console.log(`${rows.length} lignes trouvées. Upload en cours...`);

		// Insérer par batch de 100
		for (let i = 0; i < rows.length; i += 100) {
			const batch = rows.slice(i, i + 100);
			const { error } = await supabase.from('rankings').insert(batch);

			if (error) {
				console.error(`Erreur batch ${i}:`, error);
				return;
			}

			console.log(`✓ ${Math.min(i + 100, rows.length)}/${rows.length} lignes insérées`);
		}

		console.log('✅ Données chargées avec succès!');
	} catch (err) {
		console.error('Erreur:', err);
	}
}

uploadData();

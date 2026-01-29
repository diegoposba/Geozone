// Mapping des noms de catégories en base vers l'affichage français
export const categoryMapping: { [key: string]: string } = {
	'alcohol': 'Taux d\'alcool',
	'army': 'Taille de l\'armée',
	'capital_city_numeric': 'Nombre d\'habitants de la capitale',
	'capital_city_ratio': 'Ratio habitants capitale/pays',
	'chinese_diaspora': 'Nombre de chinois',
	'low_density': 'Faible densité',
	'eez': 'Zone Économique Exclusive',
	'fifa': 'Classement FIFA',
	'homicide_rate': 'Taux d\'homicides',
	'hdi': 'Indice de Développement Humain',
	'individual_gdp': 'PIB par habitant',
	'life_expectancy': 'Espérance de vie',
	'obesity': 'Taux d\'obésité',
	'olympics': 'Médailles olympiques',
	'superficy_asc': 'Petite superficie',
	'median_age': 'Âge médian',
	'sovereignty': 'Obtention de la souveraineté',
	'suicide_rate': 'Taux de suicide',
	'forest': 'Part forêt/superficie'
};

/**
 * Retourne le nom français d'une catégorie
 */
export function getCategoryDisplayName(categoryKey: string): string {
	return categoryMapping[categoryKey] || categoryKey;
}

/**
 * Sélectionne 8 catégories aléatoires parmi toutes les disponibles
 */
export function getRandomCategories(allCategories: string[], count: number = 8): string[] {
	const shuffled = [...allCategories].sort(() => Math.random() - 0.5);
	return shuffled.slice(0, count);
}

/**
 * Sélectionne un pays aléatoire parmi une liste
 */
export function getRandomCountry(countries: string[]): string {
	return countries[Math.floor(Math.random() * countries.length)];
}

/**
 * Calcule le score total d'une partie
 */
export function calculateScore(selections: {
	[category: string]: { country: string; ranking: number };
}): number {
	return Object.values(selections).reduce((sum, selection) => sum + selection.ranking, 0);
}

/**
 * Vérifie si le joueur a gagné (score < 200)
 */
export function checkWin(score: number): boolean {
	return score < 200;
}

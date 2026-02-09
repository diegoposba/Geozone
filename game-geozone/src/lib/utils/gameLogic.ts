// Mapping des noms de catégories en base vers l'affichage français
export const categoryMapping: { [key: string]: string } = {
	'alcohol': 'Taux d\'alcool',
	'army': 'Taille de l\'armée',
	'capital_city_numeric': 'Nombre d\'habitants de la capitale',
	'capital_city_ratio': 'Ratio d\'habitants capitale/pays',
	'chinese_diaspora': 'Nombre de chinois',
	'low_density': 'Faible densité',
	'eez': 'Zone Économique Exclusive (ZEE)',
	'fifa': 'Classement FIFA',
	'homicide_rate': 'Taux d\'homicides',
	'hdi': 'Indice de Développement Humain',
	'individual_gdp': 'PIB par habitant',
	'life_expectancy': 'Espérance de vie',
	'obesity': 'Taux d\'obésité',
	'olympics': 'Médailles olympiques',
	'superficy_asc': 'Petite superficie',
	'median_age': 'Faible âge médian',
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
 * @param countries Liste de tous les pays disponibles
 * @param excludeCountries Ensemble de pays à exclure (optionnel)
 */
export function getRandomCountry(countries: string[], excludeCountries?: Set<string>): string {
	let availableCountries = countries;

	// Filtrer les pays déjà utilisés
	if (excludeCountries && excludeCountries.size > 0) {
		availableCountries = countries.filter(c => !excludeCountries.has(c));
	}

	// Fallback si tous les pays sont utilisés (ne devrait pas arriver avec 192 pays et 8 tours)
	if (availableCountries.length === 0) {
		availableCountries = countries;
	}

	return availableCountries[Math.floor(Math.random() * availableCountries.length)];
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

/**
 * Calcule le meilleur score théorique possible pour les catégories sélectionnées
 * Le meilleur score = somme des rankings minimum pour chaque catégorie
 */
export function calculateTheoreticalBest(
	selectedCategories: string[],
	rankings: { country: string; [category: string]: string | number }[]
): number {
	let bestScore = 0;

	for (const category of selectedCategories) {
		let minRanking = Infinity;

		for (const ranking of rankings) {
			const value = ranking[category];
			if (typeof value === 'number' && value > 0) {
				minRanking = Math.min(minRanking, value);
			}
		}

		// Ajouter au meilleur score (si aucun ranking valide trouvé, utiliser 1 comme meilleur cas)
		bestScore += minRanking === Infinity ? 1 : minRanking;
	}

	return bestScore;
}

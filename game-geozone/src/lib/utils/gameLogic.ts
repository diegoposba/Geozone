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

// Types pour Supabase
export type User = {
	id: string;
	email: string;
	username: string;
	created_at: string;
};

export type Game = {
	id: string;
	user_id: string;
	score: number;
	categories_used: string[]; // Array des 8 catégories utilisées
	country_selections: {
		[category: string]: {
			country: string;
			ranking: number;
		};
	};
	created_at: string;
	completed_at: string | null;
	won: boolean;
};

export type Leaderboard = {
	user_id: string;
	username: string;
	total_games: number;
	best_score: number;
	average_score: number;
	win_count: number;
	win_rate: number;
};

export type Ranking = {
	id: number;
	country: string;
	[category: string]: string | number; // Dynamique pour les catégories
};

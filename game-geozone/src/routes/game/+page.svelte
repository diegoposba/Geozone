<script lang="ts">
	import { supabase } from '$lib/supabase/client';
	import { getRandomCategories, getRandomCountry, calculateScore, checkWin } from '$lib/utils/gameLogic';
	import type { Game, Ranking } from '$lib/supabase/types';
	import { onMount } from 'svelte';

	let user: any;
	let rankings: Ranking[] = [];
	let categories: string[] = [];
	let selectedCategories: string[] = [];
	let usedCategories: Set<string> = new Set();
	let currentCountry: string = '';
	let currentStep: number = 0;
	let selections: { [category: string]: { country: string; ranking: number } } = {};
	let score: number = 0;
	let gameWon: boolean | null = null;
	let loading: boolean = true;

	onMount(async () => {
		// Vérifier l'utilisateur
		const { data, error } = await supabase.auth.getSession();
		if (error || !data.session) {
			window.location.href = '/';
			return;
		}
		user = data.session.user;

		// Charger les rankings
		const { data: rankingsData, error: rankingsError } = await supabase
			.from('rankings')
			.select('*');

		if (rankingsError) {
			console.error(rankingsError);
		} else {
			rankings = rankingsData || [];
			// Extraire les catégories (colonnes sauf 'id' et 'country')
			if (rankings.length > 0) {
				categories = Object.keys(rankings[0]).filter((key) => key !== 'id' && key !== 'country');
				startNewGame();
			}
		}

		loading = false;
	});

	function startNewGame() {
		selectedCategories = getRandomCategories(categories, 8);
		usedCategories.clear();
		selections = {};
		currentStep = 0;
		score = 0;
		gameWon = null;
		pickNewCountry();
	}

	function pickNewCountry() {
		if (currentStep >= 8) {
			// Partie terminée
			endGame();
			return;
		}

		const countryList = rankings.map((r) => r.country as string);
		currentCountry = getRandomCountry(countryList);
		currentStep++;
	}

	function placeCountry(category: string) {
		if (usedCategories.has(category)) return;

		const ranking = rankings.find((r) => r.country === currentCountry);
		if (ranking) {
			selections[category] = {
				country: currentCountry,
				ranking: ranking[category] as number
			};
			usedCategories.add(category);
			score = calculateScore(selections);

			if (usedCategories.size < 8) {
				pickNewCountry();
			} else {
				endGame();
			}
		}
	}

	async function endGame() {
		gameWon = checkWin(score);

		// Sauvegarder la partie
		const { error } = await supabase.from('games').insert({
			user_id: user.id,
			score,
			categories_used: selectedCategories,
			country_selections: selections,
			completed_at: new Date().toISOString(),
			won: gameWon
		});

		if (error) {
			console.error(error);
		}
	}

	async function logout() {
		await supabase.auth.signOut();
		window.location.href = '/';
	}
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 p-6">
	<div class="mx-auto max-w-4xl">
		<!-- Header -->
		<div class="mb-8 flex items-center justify-between rounded-lg bg-white p-6 shadow-lg">
			<h1 class="text-3xl font-bold text-gray-800">GeoZone Game</h1>
			<div class="flex items-center gap-4">
				<span class="text-gray-700">{user?.email}</span>
				<button
					on:click={logout}
					class="rounded-lg bg-red-600 px-4 py-2 text-white hover:bg-red-700"
				>
					Déconnexion
				</button>
			</div>
		</div>

		{#if loading}
			<div class="text-center text-white">Chargement...</div>
		{:else if gameWon !== null}
			<!-- Fin de partie -->
			<div class="rounded-lg bg-white p-8 shadow-lg">
				<h2 class="mb-4 text-center text-2xl font-bold">
					{gameWon ? '🎉 Vous avez gagné !' : '❌ Vous avez perdu'}
				</h2>
				<p class="mb-6 text-center text-xl text-gray-700">Score: <span class="font-bold">{score}</span></p>

				<div class="mb-6 space-y-2">
					{#each selectedCategories as category}
						{@const selection = selections[category]}
						<div class="rounded-lg bg-gray-100 p-4">
							<p class="font-bold text-gray-800">{category}</p>
							<p class="text-gray-600">
								Pays: <span class="font-semibold">{selection.country}</span> - Classement: <span
									class="font-semibold">{selection.ranking}</span
								>
							</p>
						</div>
					{/each}
				</div>

				<button
					on:click={startNewGame}
					class="w-full rounded-lg bg-blue-600 px-4 py-3 font-bold text-white hover:bg-blue-700"
				>
					Nouvelle partie
				</button>
			</div>
		{:else if currentStep > 0 && currentStep <= 8}
			<!-- Pendant la partie -->
			<div class="rounded-lg bg-white p-8 shadow-lg">
				<p class="mb-2 text-center text-gray-600">Pays tiré: <span class="text-2xl font-bold">{currentCountry}</span></p>
				<p class="mb-6 text-center text-gray-600">Étape {currentStep}/8</p>

				<p class="mb-4 text-center text-lg font-bold text-gray-800">Choisissez une catégorie:</p>

				<div class="mb-6 grid grid-cols-2 gap-4">
					{#each selectedCategories as category}
						<button
							on:click={() => placeCountry(category)}
							disabled={usedCategories.has(category)}
							class="rounded-lg bg-blue-600 px-4 py-3 font-bold text-white hover:bg-blue-700 disabled:bg-gray-400"
						>
							{usedCategories.has(category) ? '✓ ' : ''}{category}
						</button>
					{/each}
				</div>

				<div class="text-center text-gray-700">
					Score actuel: <span class="text-2xl font-bold text-blue-600">{score}</span>
				</div>
			</div>
		{:else}
			<!-- Écran de démarrage -->
			<div class="text-center">
				<button
					on:click={startNewGame}
					class="rounded-lg bg-white px-8 py-4 text-2xl font-bold text-blue-600 hover:bg-gray-100"
				>
					Commencer une partie
				</button>
			</div>
		{/if}
	</div>
</div>
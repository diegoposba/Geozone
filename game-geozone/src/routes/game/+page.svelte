<script lang="ts">
	import { supabase } from '$lib/supabase/client';
	import { getRandomCategories, getRandomCountry, calculateScore, checkWin } from '$lib/utils/gameLogic';
	import Button from '$lib/components/ui/Button.svelte';
	import type { Game, Ranking } from '$lib/supabase/types';
	import { onMount } from 'svelte';

	let user: any;
	let rankings: Ranking[] = [];
	let categories: string[] = [];
	let selectedCategories: string[] = [];
	let usedCategories: Set<string> = new Set();
	let currentCountry: string = '';
	let currentCountryFlag: string = '';
	let currentStep: number = 0;
	let selections: { [category: string]: { country: string; ranking: number } } = {};
	let score: number = 0;
	let gameWon: boolean | null = null;
	let loading: boolean = true;

	// Drag & Drop
	let draggedOverCategory: string | null = null;
	let pendingCategory: string | null = null;

	const countryFlags: { [key: string]: string } = {
		'United States': '🇺🇸',
		'United Kingdom': '🇬🇧',
		'France': '🇫🇷',
		'Germany': '🇩🇪',
		'Spain': '🇪🇸',
		'Italy': '🇮🇹',
		'Canada': '🇨🇦',
		'Australia': '🇦🇺',
		'Japan': '🇯🇵',
		'China': '🇨🇳',
		'India': '🇮🇳',
		'Brazil': '🇧🇷',
		'Russia': '🇷🇺',
		'South Korea': '🇰🇷',
		'Mexico': '🇲🇽'
	};

	function handleDragStart(e: DragEvent) {
		e.dataTransfer!.effectAllowed = 'copy';
		e.dataTransfer!.setData('text/plain', currentCountry);
	}

	function handleDragOver(e: DragEvent) {
		e.preventDefault();
		e.dataTransfer!.dropEffect = 'copy';
		const category = (e.currentTarget as HTMLElement)?.dataset?.category;
		if (category && !usedCategories.has(category)) {
			draggedOverCategory = category;
		}
	}

	function handleDragLeave(e: DragEvent) {
		const category = (e.currentTarget as HTMLElement)?.dataset?.category;
		if (category === draggedOverCategory) {
			draggedOverCategory = null;
		}
	}

	function handleDrop(e: DragEvent, category: string) {
		e.preventDefault();
		if (usedCategories.has(category)) return;

		const country = e.dataTransfer!.getData('text/plain');
		if (country === currentCountry) {
			draggedOverCategory = null;
			pendingCategory = category;
		}
	}

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
		draggedOverCategory = null;
		pendingCategory = null;
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
		currentCountryFlag = countryFlags[currentCountry] || '🌍';
		currentStep++;
		pendingCategory = null;
	}

	function handleCategoryClick(category: string) {
		if (!usedCategories.has(category)) {
			pendingCategory = category;
		}
	}

	function confirmPlacement() {
		if (!pendingCategory || usedCategories.has(pendingCategory)) return;

		const ranking = rankings.find((r) => r.country === currentCountry);
		if (ranking) {
			selections[pendingCategory] = {
				country: currentCountry,
				ranking: ranking[pendingCategory] as number
			};
			usedCategories.add(pendingCategory);
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
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
	<div class="mx-auto max-w-6xl">
		{#if loading}
			<div class="flex h-96 items-center justify-center">
				<div class="text-center">
					<div class="mb-4 text-4xl">⏳</div>
					<p class="text-xl text-gray-600">Chargement du jeu...</p>
				</div>
			</div>
		{:else if gameWon !== null}
			<!-- Fin de partie -->
			<div class="rounded-xl bg-white p-8 shadow-lg">
				<div class="text-center">
					<div class="mb-4 text-6xl">{gameWon ? '🎉' : '😅'}</div>
					<h2 class="mb-2 text-4xl font-bold text-gray-800">
						{gameWon ? 'Vous avez gagné !' : 'Partie terminée'}
					</h2>
					<p class="mb-8 text-2xl font-bold text-blue-600">Score: {score}</p>
				</div>

				<div class="mb-8 space-y-3">
					{#each selectedCategories as category}
						{@const selection = selections[category]}
						<div class="flex items-center justify-between rounded-lg bg-gradient-to-r from-blue-50 to-indigo-50 p-4">
							<div>
								<p class="font-bold text-gray-800">{category}</p>
								<p class="text-sm text-gray-600">Pays: {selection.country}</p>
							</div>
							<div class="text-right">
								<div class="text-2xl font-bold text-blue-600">#{selection.ranking}</div>
								<div class="text-xs text-gray-500">Classement</div>
							</div>
						</div>
					{/each}
				</div>

				<Button variant="default" size="lg" onclick={startNewGame} class="w-full">
					🎮 Nouvelle partie
				</Button>
			</div>
		{:else if currentStep > 0 && currentStep <= 8}
			<!-- Pendant la partie -->
			<div class="space-y-6">
				<!-- Progress & Country -->
				<div class="rounded-xl bg-white p-6 shadow-lg">
					<div class="mb-4 flex items-center justify-between">
						<div>
							<p class="text-sm text-gray-600">Manche {currentStep}/8</p>
							<div class="mt-2 h-2 w-48 overflow-hidden rounded-full bg-gray-200">
								<div
									class="h-full bg-blue-600 transition-all duration-300"
									style="width: {(currentStep / 8) * 100}%"
								></div>
							</div>
						</div>
						<div class="text-right">
							<p class="text-sm text-gray-600">Score actuel</p>
							<p class="text-3xl font-bold text-blue-600">{score}</p>
						</div>
					</div>

					<div class="mt-6 text-center">
						<p class="text-sm text-gray-600 mb-3">Glissez ce pays sur une catégorie</p>
						<button
							draggable={true}
							ondragstart={handleDragStart}
							type="button"
							disabled
							class="inline-block cursor-move rounded-2xl bg-gradient-to-r from-blue-100 to-indigo-100 p-8 transition-all duration-200 hover:shadow-lg active:opacity-75 disabled:cursor-move disabled:opacity-100"
						>
							<div class="mb-3 text-6xl">{currentCountryFlag}</div>
							<p class="text-2xl font-bold text-gray-800">{currentCountry}</p>
						</button>
					</div>
				</div>

				<!-- Categories Grid -->
				<div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
					{#each selectedCategories as category}
						<div
							role="button"
							tabindex="0"
							data-category={category}
							ondragover={handleDragOver}
							ondragleave={handleDragLeave}
							ondrop={(e) => handleDrop(e, category)}
							onkeydown={(e) => {
								if (e.key === 'Enter' || e.key === ' ') {
									handleCategoryClick(category);
								}
							}}
							onclick={() => handleCategoryClick(category)}
							class={`relative rounded-xl p-6 transition-all duration-200 ${
								usedCategories.has(category)
									? 'cursor-not-allowed bg-gray-100 opacity-50'
									: draggedOverCategory === category
										? 'bg-green-100 ring-4 ring-green-500 scale-105'
										: pendingCategory === category
											? 'bg-blue-200 ring-4 ring-blue-500'
											: 'border-2 border-dashed border-gray-300 bg-white hover:border-blue-400 hover:bg-blue-50'
							}`}
						>
							<div class="text-center">
								<p class="font-bold text-gray-800">{category}</p>
								{#if pendingCategory === category}
									<p class="mt-2 text-sm text-gray-600">
										{currentCountry} en attente de validation
									</p>
									<div class="mt-4 space-y-2">
										<Button variant="default" size="sm" onclick={confirmPlacement} class="w-full">
											✓ OK
										</Button>
										<Button
											variant="outline"
											size="sm"
											onclick={() => (pendingCategory = null)}
											class="w-full"
										>
											✕ Annuler
										</Button>
									</div>
								{:else if usedCategories.has(category)}
									<div class="mt-3">
										<p class="text-sm text-gray-500">
											{selections[category].country}
										</p>
										<p class="mt-1 text-lg font-bold text-green-600">
											#{selections[category].ranking}
										</p>
									</div>
								{:else}
									<p class="mt-2 text-sm text-gray-500">Glissez le pays ici</p>
								{/if}
							</div>
						</div>
					{/each}
				</div>
			</div>
		{:else}
			<!-- Écran de démarrage -->
			<div class="flex h-96 items-center justify-center">
				<Button variant="default" size="lg" onclick={startNewGame} class="text-xl px-8 py-6">
					🎮 Commencer une partie
				</Button>
			</div>
		{/if}
	</div>
</div>
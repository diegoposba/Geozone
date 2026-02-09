<script lang="ts">
	import { supabase } from '$lib/supabase/client';
	import { getRandomCategories, getRandomCountry, calculateScore, checkWin, getCategoryDisplayName, calculateTheoreticalBest } from '$lib/utils/gameLogic';
	import { getCountryFlagUrl } from '$lib/utils/countryFlags';
	import Button from '$lib/components/ui/Button.svelte';
	import type { Game, Ranking } from '$lib/supabase/types';
	import { onMount } from 'svelte';
	import RefreshCcw from 'lucide-svelte/icons/refresh-ccw';
	import Info from 'lucide-svelte/icons/info';
	import CircleCheck from 'lucide-svelte/icons/circle-check';

	let user: any;
	let rankings: Ranking[] = [];
	let categories: string[] = [];
	let selectedCategories: string[] = [];
	let usedCategories: Set<string> = new Set();
	let usedCountries: Set<string> = new Set();
	let currentCountry: string = '';
	let currentCountryFlag: string = '';
	let currentStep: number = 0;
	let selections: { [category: string]: { country: string; ranking: number } } = {};
	let score: number = 0;
	let theoreticalBestScore: number = 0;
	let gameWon: boolean | null = null;
	let loading: boolean = true;
	let rerollsRemaining: number = 3;

	// Drag & Drop
	let draggedOverCategory: string | null = null;
	let pendingCategory: string | null = null;

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
		// Vérifier l'utilisateur (permettre l'accès invité)
		const { data, error } = await supabase.auth.getSession();
		user = data?.session?.user || null;

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
				console.log('Catégories extraites de Supabase:', categories);
				startNewGame();
			}
		}

		loading = false;
	});

	function startNewGame() {
		selectedCategories = getRandomCategories(categories, 8);
		usedCategories.clear();
		usedCountries.clear();
		selections = {};
		currentStep = 0;
		score = 0;
		theoreticalBestScore = calculateTheoreticalBest(selectedCategories, rankings);
		gameWon = null;
		rerollsRemaining = 3;
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
		currentCountry = getRandomCountry(countryList, usedCountries);
		currentCountryFlag = getCountryFlagUrl(currentCountry);
		currentStep++;
		pendingCategory = null;
	}

	function handleCategoryClick(category: string) {
		if (!usedCategories.has(category)) {
			pendingCategory = category;
		}
	}

	function handleReroll() {
		if (rerollsRemaining > 0) {
			rerollsRemaining--;
			// Relancer un pays SANS incrémenter currentStep
			const countryList = rankings.map((r) => r.country as string);
			currentCountry = getRandomCountry(countryList, usedCountries);
			currentCountryFlag = getCountryFlagUrl(currentCountry);
			pendingCategory = null;
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
			usedCountries.add(currentCountry);
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

		// Sauvegarder la partie uniquement si l'utilisateur est authentifié
		if (user && user.id) {
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
		// Les invités ne sauvegardent pas leurs parties
	}
</script>

<div class="pt-24 sm:pt-28 min-h-screen p-3 sm:p-6" style="background-color: hsl(var(--background)); color: hsl(var(--foreground))">
	<div class="mx-auto max-w-6xl">
		{#if loading}
			<div class="flex h-96 items-center justify-center">
				<div class="text-center">
					<div class="mb-4 text-4xl">⏳</div>
					<p class="text-xl">Chargement du jeu...</p>
				</div>
			</div>
		{:else if gameWon !== null}
			<!-- Fin de partie -->
			<div class="rounded-xl p-8 shadow-lg" style="background-color: hsl(var(--card)); color: hsl(var(--card-foreground))">
				<div class="text-center">
					<div class="mb-4 text-6xl">{gameWon ? '🎉' : '😅'}</div>
					<h2 class="mb-2 text-4xl font-bold" style="color: hsl(var(--primary))">
						{gameWon ? 'Vous avez gagné !' : 'Partie terminée'}
					</h2>
					<p class="mb-8 text-2xl font-bold" style="color: hsl(var(--primary))">Score: {score}</p>
				</div>

				<div class="mb-8 space-y-3">
					{#each selectedCategories as category}
						{@const selection = selections[category]}
						<div class="flex items-center justify-between rounded-lg p-4" style="background-color: hsl(var(--accent))">
							<div>
								<p class="font-bold">{getCategoryDisplayName(category)}</p>
								<p class="text-sm" style="color: hsl(var(--muted-foreground))">Pays: {selection.country}</p>
							</div>
							<div class="text-right">
								<div class="text-2xl font-bold" style="color: hsl(var(--primary))">#{selection.ranking}</div>
								<div class="text-xs" style="color: hsl(var(--muted-foreground))">Classement</div>
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
			<div class="rounded-2xl border-2 sm:border-4 border-white p-4 sm:p-8 shadow-2xl" style="background-color: hsl(var(--card)); color: hsl(var(--card-foreground))">
				<!-- Top bar -->
				<div class="mb-6 flex flex-col lg:flex-row items-center justify-between gap-4">
					<!-- Pays: X/8 -->
					<div class="text-base sm:text-lg font-bold">
						Pays: {currentStep}/8
					</div>

					<!-- Carte pays centrée + Reroll -->
					<div class="flex flex-col items-center w-full lg:w-auto">
						<div class="flex items-center gap-2">
							<button
								draggable={true}
								ondragstart={handleDragStart}
								type="button"
								disabled
								class="rounded-xl border-2 px-3 py-2 sm:px-4 sm:py-3 shadow-lg cursor-move disabled:cursor-move"
								style="background-color: hsl(var(--accent)); border-color: hsl(var(--primary))"
							>
								<div class="flex items-center justify-center gap-3">
									<img src={currentCountryFlag} alt={currentCountry} class="h-8 sm:h-10 w-auto rounded" />
									<p class="text-lg sm:text-xl font-bold">{currentCountry}</p>
								</div>
							</button>
							<Button
								size="sm"
								onclick={handleReroll}
								disabled={rerollsRemaining === 0}
							>
								<RefreshCcw /> 
							</Button>
						</div>

						<!-- Barre de progression sous le pays -->
						<div class="mt-4 w-full max-w-xs sm:w-64 h-2 overflow-hidden rounded-full" style="background-color: hsl(var(--border))">
							<div
								class="h-full transition-all duration-300"
								style="background-color: hsl(var(--primary)); width: {(currentStep / 8) * 100}%"
							></div>
						</div>
					</div>

					<!-- Score -->
					<div class="text-center lg:text-right">
						<p class="text-xs sm:text-sm" style="color: hsl(var(--muted-foreground))">Score</p>
						<p class="text-xl sm:text-2xl font-bold" style="color: hsl(var(--primary))">{score}</p>
					</div>
				</div>

				<!-- Grille 4×2 : 1 colonne mobile, 2 colonnes desktop -->
				<div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
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
							class={`relative rounded-xl p-4 transition-all duration-200 flex items-center gap-3 ${
								usedCategories.has(category)
									? 'cursor-not-allowed opacity-50'
									: draggedOverCategory === category
										? 'ring-4 scale-105'
										: pendingCategory === category
											? 'ring-4'
											: 'border-2 border-dashed'
							}`}
							style={`
								background-color: ${usedCategories.has(category) ? 'hsl(var(--muted))' : draggedOverCategory === category ? 'hsl(var(--accent))' : pendingCategory === category ? 'hsl(var(--primary))' : 'hsl(var(--card))'};
								border-color: ${draggedOverCategory === category ? 'hsl(var(--primary))' : pendingCategory === category ? 'hsl(var(--primary))' : 'hsl(var(--border))'};
								color: ${pendingCategory === category ? 'hsl(var(--primary-foreground))' : 'hsl(var(--card-foreground))'};
							`}
						>
							<!-- Icône info (gauche) -->
							<Info size={16} />

							<!-- Contenu central -->
							<div class="flex-1 flex items-center gap-2 flex-wrap">
								<p class="font-bold text-sm">{getCategoryDisplayName(category)}</p>
								{#if pendingCategory === category}
									<img src={currentCountryFlag} alt={currentCountry} class="h-5 w-auto rounded" />
									<p class="text-xs" style="color: hsl(var(--primary-foreground))">{currentCountry}</p>
									<button
										class="px-2 py-1 text-xs rounded ml-auto"
										style="background-color: hsl(var(--primary)); color: hsl(var(--primary-foreground))"
										onclick={confirmPlacement}
									>
										<CircleCheck />
									</button>
								{:else if usedCategories.has(category)}
									<img src={getCountryFlagUrl(selections[category].country)} alt={selections[category].country} class="h-5 w-auto rounded" />
									<p class="text-xs" style="color: hsl(var(--muted-foreground))">{selections[category].country}</p>
									<p class="text-sm font-bold ml-auto" style="color: hsl(var(--primary))">
										#{selections[category].ranking}
									</p>
								{:else}
									<p class="text-xs" style="color: hsl(var(--muted-foreground))">— Clique ou Drop</p>
								{/if}
							</div>

							<!-- Checkmark (droite) si rempli -->
							{#if usedCategories.has(category)}
								<div class="text-xl" style="color: #22c55e">✓</div>
							{/if}
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
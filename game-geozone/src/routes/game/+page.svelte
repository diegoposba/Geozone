<script lang="ts">
	import { supabase } from '$lib/supabase/client';
	import { getRandomCategories, getRandomCountry, calculateScore, checkWin, getCategoryDisplayName } from '$lib/utils/gameLogic';
	import { getCountryFlagUrl } from '$lib/utils/countryFlags';
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
				console.log('Catégories extraites de Supabase:', categories);
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
		currentCountry = getRandomCountry(countryList);
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
			currentCountry = getRandomCountry(countryList);
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

<div class="min-h-screen p-6" style="background-color: hsl(var(--background)); color: hsl(var(--foreground))">
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
			<div class="space-y-6">
				<!-- Progress & Country -->
				<div class="rounded-xl p-6 shadow-lg" style="background-color: hsl(var(--card)); color: hsl(var(--card-foreground))">
					<div class="mb-4 flex items-center justify-between">
						<div>
							<p class="text-sm" style="color: hsl(var(--muted-foreground))">Manche {currentStep}/8</p>
							<div class="mt-2 h-2 w-48 overflow-hidden rounded-full" style="background-color: hsl(var(--border))">
								<div
									class="h-full transition-all duration-300"
									style="background-color: hsl(var(--primary)); width: {(currentStep / 8) * 100}%"
								></div>
							</div>
						</div>
						<div class="text-right">
							<p class="text-sm" style="color: hsl(var(--muted-foreground))">Score actuel</p>
							<p class="text-3xl font-bold" style="color: hsl(var(--primary))">{score}</p>
						</div>
					</div>

					<div class="mt-6 text-center">
						<p class="text-sm mb-3" style="color: hsl(var(--muted-foreground))">Glissez ce pays sur une catégorie</p>
						<button
							draggable={true}
							ondragstart={handleDragStart}
							type="button"
							disabled
							class="inline-block cursor-move rounded-2xl p-8 transition-all duration-200 hover:shadow-lg active:opacity-75 disabled:cursor-move disabled:opacity-100"
							style="background-color: hsl(var(--accent))"
						>
							<div class="mb-3">
								<img src={currentCountryFlag} alt={currentCountry} class="h-16 w-auto mx-auto rounded" />
							</div>
							<p class="text-2xl font-bold">{currentCountry}</p>
						</button>					<div class="mt-4">
						<Button 
							variant="outline" 
							size="sm" 
							onclick={handleReroll}
							disabled={rerollsRemaining === 0}
						>
							🔄 Relancer
						</Button>
					</div>					</div>
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
							<div class="text-center">
								<p class="font-bold">{getCategoryDisplayName(category)}</p>
								{#if pendingCategory === category}
									<p class="mt-2 text-sm" style="color: hsl(var(--primary-foreground))">
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
										<p class="text-sm" style="color: hsl(var(--muted-foreground))">
											{selections[category].country}
										</p>
										<p class="mt-1 text-lg font-bold" style="color: hsl(var(--primary))">
											#{selections[category].ranking}
										</p>
									</div>
								{:else}
									<p class="mt-2 text-sm" style="color: hsl(var(--muted-foreground))">Glissez le pays ici</p>
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
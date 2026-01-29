<script lang="ts">
	import { supabase } from '$lib/supabase/client';
	import Button from '$lib/components/ui/Button.svelte';
	import { onMount } from 'svelte';

	let user: any = null;
	let loading = true;

	onMount(async () => {
		const { data, error } = await supabase.auth.getSession();
		if (error || !data.session) {
			window.location.href = '/';
			return;
		}
		user = data.session.user;
		loading = false;
	});

	function startGame() {
		window.location.href = '/game';
	}
</script>

{#if !loading}
	<div class="min-h-screen py-12 px-4" style="background-color: hsl(var(--background)); color: hsl(var(--foreground))">
		<div class="mx-auto max-w-4xl">
			<!-- Welcome Section -->
			<div class="mb-12 text-center">
				<h1 class="mb-4 text-5xl font-bold" style="color: hsl(var(--primary))">Bienvenue sur GeoZone! 🌍</h1>
				<p class="text-xl" style="color: hsl(var(--muted-foreground))">
					Testez vos connaissances en géographie et devenez un véritable expert du monde
				</p>
			</div>

			<!-- Game Rules Section -->
			<div class="mb-12 grid gap-8 md:grid-cols-2">
				<div class="rounded-xl p-8 shadow-lg" style="background-color: hsl(var(--card)); color: hsl(var(--card-foreground))">
					<h2 class="mb-6 text-2xl font-bold" style="color: hsl(var(--primary))">📋 Règles du jeu</h2>
					<ul class="space-y-4">
						<li class="flex gap-3">
							<span class="text-2xl">1️⃣</span>
							<div>
								<strong>Pays aléatoire :</strong> Un pays et son drapeau vous seront présentés à chaque manche
							</div>
						</li>
						<li class="flex gap-3">
							<span class="text-2xl">2️⃣</span>
							<div>
								<strong>Classement :</strong> Classez le pays dans une catégorie en le glissant-déposant
							</div>
						</li>
						<li class="flex gap-3">
							<span class="text-2xl">3️⃣</span>
							<div>
								<strong>Validation :</strong> Cliquez sur "OK" pour valider votre choix
							</div>
						</li>
						<li class="flex gap-3">
							<span class="text-2xl">4️⃣</span>
							<div>
								<strong>Score :</strong> Gagnez des points selon votre précision
							</div>
						</li>
						<li class="flex gap-3">
							<span class="text-2xl">5️⃣</span>
							<div>
								<strong>8 manches :</strong> Complétez 8 manches pour terminer la partie
							</div>
						</li>
					</ul>
				</div>

				<!-- Categories Section -->
				<div class="rounded-xl p-8 shadow-lg" style="background-color: hsl(var(--card)); color: hsl(var(--card-foreground))">
					<h2 class="mb-6 text-2xl font-bold" style="color: hsl(var(--primary))">📊 Catégories</h2>
					<div class="grid grid-cols-2 gap-4">
						<div class="rounded-lg p-4 text-center" style="background-color: hsl(var(--accent))">
							<div class="text-2xl">🏛️</div>
							<div class="mt-2 font-semibold">Capitales</div>
						</div>
						<div class="rounded-lg p-4 text-center" style="background-color: hsl(var(--accent))">
							<div class="text-2xl">📏</div>
							<div class="mt-2 font-semibold">Superficie</div>
						</div>
						<div class="rounded-lg p-4 text-center" style="background-color: hsl(var(--accent))">
							<div class="text-2xl">👥</div>
							<div class="mt-2 font-semibold">Population</div>
						</div>
						<div class="rounded-lg p-4 text-center" style="background-color: hsl(var(--accent))">
							<div class="text-2xl">💰</div>
							<div class="mt-2 font-semibold">Économie</div>
						</div>
						<div class="rounded-lg p-4 text-center" style="background-color: hsl(var(--accent))">
							<div class="text-2xl">⛰️</div>
							<div class="mt-2 font-semibold">Altitude</div>
						</div>
						<div class="rounded-lg p-4 text-center" style="background-color: hsl(var(--accent))">
							<div class="text-2xl">🌊</div>
							<div class="mt-2 font-semibold">Océans</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Tips Section -->
			<div class="mb-12 rounded-xl p-8 shadow-lg" style="background-color: hsl(var(--accent))">
				<h2 class="mb-4 text-2xl font-bold" style="color: hsl(var(--primary))">💡 Conseils</h2>
				<ul class="space-y-2">
					<li>• Écoutez votre instinct : le premier classement est souvent le bon !</li>
					<li>• Observez bien les variations du classement pour chaque catégorie</li>
					<li>• Les petits pays peuvent être dans le top 10 pour certaines catégories (ex: PIB par habitant)</li>
					<li>• Utilisez vos connaissances générales en géographie et économie</li>
				</ul>
			</div>

			<!-- CTA Section -->
			<div class="text-center">
				<Button
					variant="default"
					size="lg"
					onclick={startGame}
					class="text-lg"
				>
					🎮 Commencer une partie
				</Button>
			</div>
		</div>
	</div>
{/if}

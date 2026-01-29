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
	<div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
		<div class="mx-auto max-w-4xl">
			<!-- Welcome Section -->
			<div class="mb-12 text-center">
				<h1 class="mb-4 text-5xl font-bold text-gray-800">Bienvenue sur GeoZone! 🌍</h1>
				<p class="text-xl text-gray-600">
					Testez vos connaissances en géographie et devenez un véritable expert du monde
				</p>
			</div>

			<!-- Game Rules Section -->
			<div class="mb-12 grid gap-8 md:grid-cols-2">
				<div class="rounded-xl bg-white p-8 shadow-lg">
					<h2 class="mb-6 text-2xl font-bold text-blue-600">📋 Règles du jeu</h2>
					<ul class="space-y-4 text-gray-700">
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
				<div class="rounded-xl bg-white p-8 shadow-lg">
					<h2 class="mb-6 text-2xl font-bold text-blue-600">📊 Catégories</h2>
					<div class="grid grid-cols-2 gap-4">
						<div class="rounded-lg bg-blue-100 p-4 text-center">
							<div class="text-2xl">🏛️</div>
							<div class="mt-2 font-semibold text-gray-800">Capitales</div>
						</div>
						<div class="rounded-lg bg-green-100 p-4 text-center">
							<div class="text-2xl">📏</div>
							<div class="mt-2 font-semibold text-gray-800">Superficie</div>
						</div>
						<div class="rounded-lg bg-red-100 p-4 text-center">
							<div class="text-2xl">👥</div>
							<div class="mt-2 font-semibold text-gray-800">Population</div>
						</div>
						<div class="rounded-lg bg-purple-100 p-4 text-center">
							<div class="text-2xl">💰</div>
							<div class="mt-2 font-semibold text-gray-800">Économie</div>
						</div>
						<div class="rounded-lg bg-orange-100 p-4 text-center">
							<div class="text-2xl">⛰️</div>
							<div class="mt-2 font-semibold text-gray-800">Altitude</div>
						</div>
						<div class="rounded-lg bg-cyan-100 p-4 text-center">
							<div class="text-2xl">🌊</div>
							<div class="mt-2 font-semibold text-gray-800">Océans</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Tips Section -->
			<div class="mb-12 rounded-xl bg-yellow-50 p-8 shadow-lg">
				<h2 class="mb-4 text-2xl font-bold text-yellow-800">💡 Conseils</h2>
				<ul class="space-y-2 text-gray-700">
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

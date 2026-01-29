<script lang="ts">
	import { supabase } from '$lib/supabase/client';
	import Button from './ui/Button.svelte';

	let isLoading = $state(false);

	async function handleLogout() {
		isLoading = true;
		const { error } = await supabase.auth.signOut();
		if (!error) {
			window.location.href = '/';
		}
		isLoading = false;
	}
</script>

<header class="border-b border-gray-200 bg-white shadow">
	<div class="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
		<div class="flex items-center gap-8">
			<a href="/" class="flex items-center gap-2 text-2xl font-bold text-blue-600">
				<span>🌍</span>
				<span>GeoZone</span>
			</a>
			<nav class="flex gap-6">
				<a href="/home" class="text-gray-700 hover:text-blue-600">Accueil</a>
				<a href="/game" class="text-gray-700 hover:text-blue-600">Jeu</a>
			</nav>
		</div>

		<div class="flex items-center gap-4">
			<button class="text-gray-700 hover:text-blue-600">👤</button>
			<Button
				variant="destructive"
				size="sm"
				onclick={handleLogout}
			>
				{isLoading ? 'Déconnexion...' : 'Déconnexion'}
			</Button>
		</div>
	</div>
</header>

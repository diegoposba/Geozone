<script lang="ts">
	import { supabase } from '$lib/supabase/client';
	import Button from './ui/Button.svelte';

	let isLoading = $state(false);
	let homeHover = $state(false);
	let gameHover = $state(false);

	async function handleLogout() {
		isLoading = true;
		const { error } = await supabase.auth.signOut();
		if (!error) {
			window.location.href = '/';
		}
		isLoading = false;
	}
</script>

<header class="border-b shadow-md" style="background-color: hsl(var(--card)); border-color: hsl(var(--border))">
	<div class="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
		<div class="flex items-center gap-8">
			<a href="/" class="flex items-center gap-2 text-2xl font-bold" style="color: hsl(var(--primary))">
				<span>🌍</span>
				<span>GeoZone</span>
			</a>
			<nav class="flex gap-6">
				<a 
					href="/home" 
					class="transition-colors" 
					style="color: {homeHover ? 'hsl(var(--primary))' : 'hsl(var(--foreground))'}"
					onmouseenter={() => homeHover = true}
					onmouseleave={() => homeHover = false}
				>
					Accueil
				</a>
				<a 
					href="/game" 
					class="transition-colors" 
					style="color: {gameHover ? 'hsl(var(--primary))' : 'hsl(var(--foreground))'}"
					onmouseenter={() => gameHover = true}
					onmouseleave={() => gameHover = false}
				>
					Jeu
				</a>
			</nav>
		</div>

		<div class="flex items-center gap-4">
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

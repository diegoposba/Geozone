<script lang="ts">
	import { supabase } from '$lib/supabase/client';
	import Button from './ui/Button.svelte';

	let isLoading = $state(false);
	let homeHover = $state(false);
	let gameHover = $state(false);
	let user: any = $state(null);

	// Vérifier la session utilisateur
	$effect(() => {
		if (typeof window !== 'undefined') {
			supabase.auth.getSession().then(({ data }) => {
				user = data?.session?.user || null;
			});
		}
	});

	async function handleLogout() {
		isLoading = true;
		const { error } = await supabase.auth.signOut();
		if (!error) {
			window.location.href = '/';
		}
		isLoading = false;
	}
</script>

<header class="fixed top-4 left-1/2 -translate-x-1/2 z-50 border shadow-md rounded-lg backdrop-blur-md" style="background-color: hsla(var(--card-hue), var(--card-sat), var(--card-light), 0.7); border-color: hsl(var(--border)); width: calc(100% - 2rem); max-width: 90rem; background: rgba(42, 48, 64, 0.7); border: 1px solid rgba(61, 67, 84, 0.5);">
	<div class="mx-auto flex flex-col sm:flex-row max-w-7xl items-center justify-between px-4 sm:px-6 py-3 sm:py-4 w-full gap-4 sm:gap-0">
		<div class="flex items-center justify-between w-full sm:w-auto gap-4 sm:gap-8">
			<a href="/" class="flex items-center gap-2 text-xl sm:text-2xl font-bold" style="color: hsl(var(--primary))">
				<span>🌍</span>
				<span>GeoHunter</span>
			</a>
			<nav class="flex flex-wrap gap-3 sm:gap-6 items-center justify-center">
				<a
					href="/home"
					class="transition-colors text-sm sm:text-base"
					style="color: {homeHover ? 'hsl(var(--primary))' : 'hsl(var(--foreground))'}"
					onmouseenter={() => homeHover = true}
					onmouseleave={() => homeHover = false}
				>
					Accueil
				</a>
				<span class="hidden sm:inline" style="color: hsl(var(--muted-foreground))">|</span>
				<a
					href="/game"
					class="transition-colors text-sm sm:text-base"
					style="color: {gameHover ? 'hsl(var(--primary))' : 'hsl(var(--foreground))'}"
					onmouseenter={() => gameHover = true}
					onmouseleave={() => gameHover = false}
				>
					Jeux
				</a>
				<span class="hidden sm:inline" style="color: hsl(var(--muted-foreground))">|</span>
				<a
					href="/leaderboard"
					class="transition-colors text-sm sm:text-base"
					style="color: hsl(var(--foreground))"
				>
					Classement
				</a>
			</nav>
		</div>

		<div class="flex items-center gap-2 sm:gap-4">
			{#if user}
				<Button
					variant="destructive"
					size="sm"
					onclick={handleLogout}
				>
					{isLoading ? 'Déco...' : 'Déconnexion'}
				</Button>
			{:else}
				<Button
					variant="default"
					size="sm"
					onclick={() => window.location.href = '/'}
				>
					Connexion
				</Button>
			{/if}
		</div>
	</div>
</header>

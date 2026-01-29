<script lang="ts">
	import { supabase } from '$lib/supabase/client';
	import Button from '$lib/components/ui/Button.svelte';

	let email = '';
	let password = '';
	let isSignUp = false;
	let loading = false;
	let error = '';

	async function handleAuth() {
		loading = true;
		error = '';

		try {
			if (isSignUp) {
				const { error: signUpError } = await supabase.auth.signUp({
					email,
					password
				});
				if (signUpError) throw signUpError;
				error = 'Inscription réussie ! Vérifiez votre email.';
			} else {
				const { error: signInError } = await supabase.auth.signInWithPassword({
					email,
					password
				});
				if (signInError) throw signInError;
				// Redirection vers la page d'accueil
				window.location.href = '/home';
			}
		} catch (err: any) {
			error = err.message;
		} finally {
			loading = false;
		}
	}
</script>

<div class="flex min-h-screen items-center justify-center" style="background-color: hsl(var(--background))">
	<div class="w-full max-w-md rounded-lg p-8 shadow-2xl" style="background-color: hsl(var(--card)); color: hsl(var(--card-foreground))">
		<div class="mb-6 text-center">
			<div class="mb-4 text-5xl">🌍</div>
			<h1 class="text-3xl font-bold text-gray-800">GeoZone Game</h1>
			<p class="mt-2 text-gray-600">Testez vos connaissances géographiques</p>
		</div>

		{#if error}
			<div class={`mb-4 rounded-lg p-4 ${error.includes('Inscription réussie') ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
				{error}
			</div>
		{/if}

		<form onsubmit={(e) => { e.preventDefault(); handleAuth(); }} class="space-y-4">
			<input
				type="email"
				placeholder="Email"
				bind:value={email}
				required
				class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
			/>

			<input
				type="password"
				placeholder="Mot de passe"
				bind:value={password}
				required
				class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
			/>

			<Button
				type="submit"
				disabled={loading}
				class="w-full"
			>
				{loading ? 'Chargement...' : isSignUp ? 'S\'inscrire' : 'Se connecter'}
			</Button>
		</form>

		<button
			type="button"
			onclick={() => (isSignUp = !isSignUp)}
			class="mt-4 w-full text-center text-sm text-gray-600 hover:text-blue-600"
		>
			{isSignUp ? 'Déjà inscrit ? Se connecter' : 'Pas inscrit ? S\'inscrire'}
		</button>
	</div>
</div>

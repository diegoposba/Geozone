<script lang="ts">
	import { supabase } from '$lib/supabase/client';

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
				// Redirection vers le jeu
				window.location.href = '/game';
			}
		} catch (err: any) {
			error = err.message;
		} finally {
			loading = false;
		}
	}
</script>

<div class="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600">
	<div class="w-full max-w-md rounded-lg bg-white p-8 shadow-lg">
		<h1 class="mb-6 text-center text-3xl font-bold text-gray-800">GeoZone Game</h1>

		{#if error}
			<div class="mb-4 rounded-lg bg-red-100 p-4 text-red-700">{error}</div>
		{/if}

		<form on:submit|preventDefault={handleAuth} class="space-y-4">
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

			<button
				type="submit"
				disabled={loading}
				class="w-full rounded-lg bg-blue-600 px-4 py-2 font-bold text-white hover:bg-blue-700 disabled:opacity-50"
			>
				{loading ? 'Chargement...' : isSignUp ? 'S\'inscrire' : 'Se connecter'}
			</button>
		</form>

		<button
			on:click={() => (isSignUp = !isSignUp)}
			class="mt-4 w-full text-center text-sm text-gray-600 hover:text-blue-600"
		>
			{isSignUp ? 'Déjà inscrit ? Se connecter' : 'Pas inscrit ? S\'inscrire'}
		</button>
	</div>
</div>

<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import Header from '$lib/components/Header.svelte';
	import { supabase } from '$lib/supabase/client';

	let { children } = $props();
	let user: any = $state(null);
	let isOnAuthPage: boolean = $state(false);

	$effect(() => {
		if (typeof window !== 'undefined') {
			isOnAuthPage = window.location.pathname === '/';
		}
	});

	// Appliquer le mode dark par défaut
	$effect(() => {
		if (typeof document !== 'undefined') {
			document.documentElement.classList.add('dark');
		}
	});

	// Vérifier la session utilisateur
	$effect(() => {
		if (typeof window !== 'undefined') {
			supabase.auth.getSession().then(({ data }) => {
				user = data?.session?.user;
			});
		}
	});
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>

{#if !isOnAuthPage}
	<Header />
{/if}

<main>
	{@render children()}
</main>


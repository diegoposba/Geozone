<script lang="ts">
	import { cn } from '$lib/utils/cn';

	interface Props {
		variant?:
			| 'default'
			| 'destructive'
			| 'outline'
			| 'secondary'
			| 'ghost'
			| 'link';
		size?: 'default' | 'sm' | 'lg' | 'icon';
		class?: string;
		disabled?: boolean;
		type?: 'button' | 'submit' | 'reset';
		onclick?: (e?: Event) => void;
	}

	let {
		class: className,
		variant = 'default',
		size = 'default',
		disabled = false,
		type = 'button',
		onclick,
		children
	}: Props & { children: any } = $props();

	const variants = {
		default: 'bg-blue-600 text-white hover:bg-blue-700',
		destructive: 'bg-red-600 text-white hover:bg-red-700',
		outline: 'border border-gray-300 bg-white hover:bg-gray-100',
		secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
		ghost: 'hover:bg-gray-100',
		link: 'text-blue-600 underline'
	};

	const sizes = {
		default: 'h-10 px-4 py-2',
		sm: 'h-8 px-3 text-sm',
		lg: 'h-12 px-6 text-lg',
		icon: 'h-10 w-10'
	};
</script>

<button
	{type}
	{disabled}
	{onclick}
	class={cn(
		'inline-flex items-center justify-center whitespace-nowrap rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed',
		variants[variant],
		sizes[size],
		className
	)}
>
	{#if children}
		{@render children()}
	{/if}
</button>

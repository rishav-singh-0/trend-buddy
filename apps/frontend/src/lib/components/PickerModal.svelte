<script lang="ts">
	import { browser } from '$app/environment';
	import { createEventDispatcher, tick } from 'svelte';

	export type PickerItem = {
		id: string;
		label: string;
		meta?: string;
		description?: string;
		badge?: string;
	};

	export let open = false;
	export let title = 'Select item';
	export let placeholder = 'Search';
	export let query = '';
	export let items: PickerItem[] = [];
	export let selectedId = '';
	export let emptyMessage = 'No matches found.';

	const dispatch = createEventDispatcher<{
		close: void;
		queryChange: string;
		select: string;
	}>();

	let inputElement: HTMLInputElement | null = null;

	function closeModal() {
		dispatch('close');
	}

	function handleBackdropClick(event: MouseEvent) {
		if (event.target === event.currentTarget) {
			closeModal();
		}
	}

	function handleItemSelect(id: string) {
		dispatch('select', id);
	}

	$: if (browser && open) {
		tick().then(() => {
			inputElement?.focus();
		});
	}
</script>

{#if open}
	<div class="picker-backdrop" role="presentation" on:click={handleBackdropClick}>
		<section
			class="picker-modal"
			role="dialog"
			aria-modal="true"
			aria-label={title}
			on:click|stopPropagation={() => {}}
		>
			<header class="picker-header">
				<div>
					<p>{title}</p>
					<small>{items.length} matches</small>
				</div>
				<button type="button" aria-label={`Close ${title}`} on:click={closeModal}>Close</button>
			</header>

			<div class="picker-search">
				<input
					bind:this={inputElement}
					type="text"
					value={query}
					placeholder={placeholder}
					autocomplete="off"
					on:input={(event) => dispatch('queryChange', (event.currentTarget as HTMLInputElement).value)}
				/>
			</div>

			<div class="picker-results">
				{#if items.length}
					{#each items as item}
						<button
							type="button"
							class:selected={item.id === selectedId}
							class="picker-item"
							on:click={() => handleItemSelect(item.id)}
						>
							<div class="picker-copy">
								<strong>{item.label}</strong>
								{#if item.meta}
									<span>{item.meta}</span>
								{/if}
								{#if item.description}
									<small>{item.description}</small>
								{/if}
							</div>
							{#if item.badge}
								<em>{item.badge}</em>
							{/if}
						</button>
					{/each}
				{:else}
					<div class="picker-empty">{emptyMessage}</div>
				{/if}
			</div>
		</section>
	</div>
{/if}

<style>
	.picker-backdrop {
		position: fixed;
		inset: 0;
		z-index: 30;
		display: grid;
		place-items: center;
		padding: 24px;
		background: rgba(8, 9, 12, 0.76);
		backdrop-filter: blur(14px);
	}

	.picker-modal {
		width: min(720px, 100%);
		max-height: min(620px, calc(100vh - 48px));
		display: grid;
		grid-template-rows: auto auto minmax(0, 1fr);
		overflow: hidden;
		border: 1px solid #2c2f39;
		border-radius: 18px;
		background: linear-gradient(180deg, #171b26, #11141d);
		box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
	}

	.picker-header {
		display: flex;
		align-items: start;
		justify-content: space-between;
		gap: 16px;
		padding: 18px 20px 14px;
		border-bottom: 1px solid #272b37;
	}

	.picker-header p,
	.picker-header small,
	.picker-copy strong,
	.picker-copy span,
	.picker-copy small,
	.picker-empty,
	.picker-item em {
		margin: 0;
	}

	.picker-header p {
		font-size: 0.95rem;
		font-weight: 600;
		color: #edf1f8;
	}

	.picker-header small {
		display: block;
		margin-top: 0.25rem;
		color: #7f889a;
		font-size: 0.74rem;
		text-transform: uppercase;
		letter-spacing: 0.1em;
	}

	.picker-header button,
	.picker-item {
		border: none;
		cursor: pointer;
	}

	.picker-header button {
		padding: 0.55rem 0.85rem;
		border-radius: 999px;
		background: #232838;
		color: #cfd7e7;
	}

	.picker-search {
		padding: 14px 20px;
		border-bottom: 1px solid #272b37;
	}

	.picker-search input {
		width: 100%;
		padding: 0.95rem 1rem;
		border: 1px solid #2f3547;
		border-radius: 14px;
		background: #111521;
		color: #ecf2ff;
	}

	.picker-results {
		overflow-y: auto;
		padding: 8px;
	}

	.picker-item {
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 16px;
		padding: 14px 12px;
		border-radius: 12px;
		background: transparent;
		color: inherit;
		text-align: left;
	}

	.picker-item:hover,
	.picker-item.selected {
		background: rgba(87, 127, 255, 0.12);
	}

	.picker-copy {
		display: grid;
		gap: 0.28rem;
	}

	.picker-copy strong {
		color: #edf1f8;
		font-size: 0.95rem;
	}

	.picker-copy span {
		color: #9ea9be;
		font-size: 0.82rem;
	}

	.picker-copy small {
		color: #717b91;
		font-size: 0.76rem;
	}

	.picker-item em {
		font-style: normal;
		padding: 0.3rem 0.55rem;
		border-radius: 999px;
		background: #232838;
		color: #9bb1ff;
		font-size: 0.74rem;
	}

	.picker-empty {
		padding: 32px 18px;
		color: #8c94a7;
		text-align: center;
	}
</style>

<script lang="ts">
	import type { MarketSnapshot } from '$lib/types';

	export let tick: MarketSnapshot | null = null;
	export let connectionState = 'connecting';

	$: priceTone = tick && tick.change_pct >= 0 ? 'positive' : 'negative';
</script>

<section class="panel live">
	<div class="label-row">
		<p class="eyebrow">Live pulse</p>
		<span class:online={connectionState === 'connected'}>{connectionState}</span>
	</div>

	{#if tick}
		<div class="price-row">
			<strong>{tick.symbol}</strong>
			<div>
				<p class="price">{tick.price.toFixed(2)}</p>
				<p class={`delta ${priceTone}`}>{tick.change_pct.toFixed(2)}%</p>
			</div>
		</div>
		<p class="signal">Current bias: {tick.signal}</p>
		<p class="stamp">Updated {new Date(tick.generated_at).toLocaleTimeString()}</p>
	{:else}
		<p class="empty">Waiting for the market stream.</p>
	{/if}
</section>

<style>
	.live {
		display: grid;
		gap: 1rem;
	}

	.label-row,
	.price-row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1rem;
	}

	.eyebrow,
	.signal,
	.stamp,
	.empty {
		margin: 0;
	}

	.eyebrow,
	.stamp,
	.empty {
		color: rgba(245, 245, 240, 0.72);
		font-size: 0.92rem;
	}

	.price {
		margin: 0;
		font-size: clamp(1.6rem, 4vw, 2.4rem);
		font-weight: 700;
	}

	.delta {
		margin: 0.25rem 0 0;
		font-size: 0.95rem;
	}

	.positive {
		color: #86efac;
	}

	.negative {
		color: #fca5a5;
	}

	span {
		border: 1px solid rgba(245, 245, 240, 0.15);
		border-radius: 999px;
		padding: 0.25rem 0.7rem;
		font-size: 0.75rem;
		text-transform: capitalize;
	}

	.online {
		border-color: rgba(134, 239, 172, 0.5);
		color: #86efac;
	}
</style>

<script lang="ts">
	import type { MarketSnapshot } from '$lib/types';

	export let tick: MarketSnapshot | null = null;
	export let connectionState = 'connecting';

	$: priceTone = tick && tick.change_pct >= 0 ? 'positive' : 'negative';
</script>

<section class="ticker-card card">
	<div class="card-head">
		<div>
			<p class="section-kicker">Live pulse</p>
			<h2>NIFTY stream</h2>
		</div>
		<span class:online={connectionState === 'connected'}>{connectionState}</span>
	</div>

	{#if tick}
		<div class="price-stack">
			<strong>{tick.symbol}</strong>
			<p class="price">{tick.price.toFixed(2)}</p>
			<p class={`delta ${priceTone}`}>{tick.change_pct.toFixed(2)}%</p>
		</div>

		<div class="detail-grid">
			<div>
				<span>Signal</span>
				<strong>{tick.signal}</strong>
			</div>
			<div>
				<span>Updated</span>
				<strong>{new Date(tick.generated_at).toLocaleTimeString()}</strong>
			</div>
		</div>
	{:else}
		<p class="empty-text">Waiting for websocket market updates.</p>
	{/if}
</section>

<style>
	.card {
		background: rgba(255, 255, 255, 0.92);
		border: 1px solid rgba(148, 163, 184, 0.18);
		border-radius: 24px;
		box-shadow: 0 18px 50px rgba(15, 23, 42, 0.06);
		padding: 1.25rem;
	}

	.ticker-card {
		display: grid;
		gap: 1rem;
	}

	.card-head,
	.detail-grid {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1rem;
	}

	.section-kicker,
	h2,
	strong,
	p,
	span {
		margin: 0;
	}

	.section-kicker {
		text-transform: uppercase;
		letter-spacing: 0.12em;
		font-size: 0.72rem;
		font-weight: 700;
		color: #387ed1;
		margin-bottom: 0.3rem;
	}

	h2 {
		font-size: 1.1rem;
		letter-spacing: -0.02em;
	}

	span {
		display: inline-flex;
		align-items: center;
		border-radius: 999px;
		padding: 0.35rem 0.75rem;
		font-size: 0.76rem;
		text-transform: capitalize;
		background: #f1f5f9;
		color: #64748b;
	}

	.online {
		background: rgba(22, 163, 74, 0.12);
		color: #15803d;
	}

	.price-stack {
		padding: 1rem;
		border-radius: 20px;
		background: linear-gradient(180deg, #f8fbff, #f3f7fd);
		border: 1px solid #e1ebf8;
	}

	.price-stack strong {
		font-size: 0.88rem;
		color: #475569;
	}

	.price {
		font-size: clamp(2rem, 4vw, 2.4rem);
		line-height: 1;
		color: #0f172a;
		margin: 0.35rem 0;
	}

	.delta {
		font-size: 0.92rem;
		font-weight: 700;
	}

	.positive {
		color: #16a34a;
	}

	.negative {
		color: #dc2626;
	}

	.detail-grid {
		align-items: stretch;
	}

	.detail-grid div {
		flex: 1;
		padding: 0.9rem 1rem;
		border-radius: 18px;
		background: #f8fafc;
	}

	.detail-grid div span {
		padding: 0;
		background: transparent;
		font-size: 0.75rem;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: #94a3b8;
		margin-bottom: 0.35rem;
	}

	.detail-grid div strong {
		color: #0f172a;
	}

	.empty-text {
		color: #64748b;
	}

	@media (max-width: 720px) {
		.card-head,
		.detail-grid {
			flex-direction: column;
			align-items: start;
		}

		.detail-grid {
			width: 100%;
		}

		.detail-grid div {
			width: 100%;
		}
	}
</style>

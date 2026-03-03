import csv
import math
import numpy as np
import time

def get_score_numpy(slope, phase, idxs, tgts, obligs, func_type):
	vals = slope * idxs + phase
	if func_type == 'floor':
		preds = np.floor(vals).astype(np.int64)
	elif func_type == 'ceil':
		preds = np.ceil(vals).astype(np.int64)
	else:
		preds = np.round(vals).astype(np.int64)

	matches = (preds == tgts)
	total_matches = np.sum(matches)
	oblig_matches = np.sum(matches & obligs)
	return int(total_matches), int(oblig_matches)

def optimize_for_func(func_type, indices, targets, is_oblig, slope_lr, phase_lr, count):
	print(f"\nOptimizing for math.{func_type}...")

	idxs_np = np.array(indices)
	tgts_np = np.array(targets)
	obligs_np = np.array(is_oblig)

	sample_indices = idxs_np[::20]
	sample_targets = tgts_np[::20]
	sample_is_oblig = obligs_np[::20]

	# Coarse Search for Phase using sample
	print("Performing coarse search for Phase (sampled)...")
	best_coarse_p = phase_lr
	best_coarse_o = -1
	best_coarse_m = -1

	scan_range = 2000
	step_coarse = 0.001

	# Vectorize coarse search
	phases = phase_lr + np.arange(-scan_range, scan_range + 1) * step_coarse
	for p in phases:
		m, o = get_score_numpy(slope_lr, p, sample_indices, sample_targets, sample_is_oblig, func_type)
		if o > best_coarse_o or (o == best_coarse_o and m > best_coarse_m):
			best_coarse_o = o
			best_coarse_m = m
			best_coarse_p = p

	print(f"Best Coarse Phase: {best_coarse_p}")

	print(f"\n{'Prec':<5} {'Slope':<20} {'Phase':<20} {'Oblig Acc':<10} {'Total Acc':<10}")
	print("-" * 75)

	best_known_s = slope_lr
	best_known_p = best_coarse_p

	final_best_params = (best_known_s, best_known_p)
	final_best_oblig = 0
	final_best_total = 0

	for precision in range(4, 11):
		step = 10**(-precision)

		current_s = round(best_known_s, precision)
		current_p = round(best_known_p, precision)

		best_params = (current_s, current_p)
		m, o = get_score_numpy(current_s, current_p, idxs_np, tgts_np, obligs_np, func_type)
		best_oblig = o
		best_total = m

		max_iter = 5
		search_range = 100

		for _ in range(max_iter):
			changed = False

			# Optimize Phase
			best_p_local = best_params[1]
			best_o_local = best_oblig
			best_m_local = best_total

			for dp in range(-search_range, search_range + 1):
				if dp == 0: continue
				p = round(best_params[1] + dp * step, precision)
				m_new, o_new = get_score_numpy(best_params[0], p, idxs_np, tgts_np, obligs_np, func_type)

				if o_new > best_o_local or (o_new == best_o_local and m_new > best_m_local):
					best_o_local = o_new
					best_m_local = m_new
					best_p_local = p
					changed = True

			best_params = (best_params[0], best_p_local)
			best_oblig = best_o_local
			best_total = best_m_local

			# Optimize Slope
			best_s_local = best_params[0]
			best_o_local = best_oblig
			best_m_local = best_total

			for ds in range(-search_range, search_range + 1):
				if ds == 0: continue
				s = round(best_params[0] + ds * step, precision)
				m_new, o_new = get_score_numpy(s, best_params[1], idxs_np, tgts_np, obligs_np, func_type)

				if o_new > best_o_local or (o_new == best_o_local and m_new > best_m_local):
					best_o_local = o_new
					best_m_local = m_new
					best_s_local = s
					changed = True

			best_params = (best_s_local, best_params[1])
			best_oblig = best_o_local
			best_total = best_m_local

			if not changed:
				break

		best_known_s = best_params[0]
		best_known_p = best_params[1]

		total_oblig = np.sum(is_oblig)
		oblig_pct = (best_oblig / total_oblig) * 100
		total_pct = (best_total / count) * 100

		print(f"{precision:<5} {best_params[0]:<20} {best_params[1]:<20} {best_oblig:<10} ({oblig_pct:.2f}%) {best_total:<10} ({total_pct:.2f}%)")

		if best_oblig > final_best_oblig or (best_oblig == final_best_oblig and best_total > final_best_total):
			final_best_oblig = best_oblig
			final_best_total = best_total
			final_best_params = best_params

	print("-" * 75)
	return final_best_params, final_best_oblig, final_best_total

def optimize():
	data = []
	csv_file = 'gt_1_10000.csv'
	try:
		with open(csv_file, 'r') as f:
			reader = csv.reader(f)
			next(reader) # skip header
			for row in reader:
				data.append((int(row[0]), int(row[1])))
	except FileNotFoundError:
		print(f"{csv_file} not found.")
		return

	count = len(data)
	print(f"Loaded {count} records from {csv_file}.")

	oblig_indices = {8, 9, 11}
	indices = [d[0] for d in data]
	jds = [d[1] for d in data]
	is_oblig = [(i % 12) in oblig_indices for i in indices]

	epoch = 1948440
	targets = [jd - epoch for jd in jds]

	# Linear Regression
	n = count
	sum_x = sum(indices)
	sum_y = sum(targets)
	sum_xy = sum(x*y for x, y in zip(indices, targets))
	sum_xx = sum(x*x for x in indices)

	slope_lr = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)
	intercept_lr = (sum_y - slope_lr * sum_x) / n
	phase_lr = intercept_lr

	print(f"Initial Guess (Linear Regression):")
	print(f"Slope: {slope_lr}")
	print(f"Phase: {phase_lr}")

	results = []

	for func_type in ["floor", "ceil", "round"]:
		params, oblig, total = optimize_for_func(func_type, indices, targets, is_oblig, slope_lr, phase_lr, count)
		results.append((func_type, params, oblig, total))

	print("\nSummary Comparison:")
	print(f"{'Method':<12} {'Best Slope':<20} {'Best Phase':<20} {'Oblig Acc':<15} {'Total Acc':<15}")
	total_oblig = sum(is_oblig)
	for name, params, oblig, total in results:
		print(f"math.{name:<7} {params[0]:<20} {params[1]:<20} {oblig:<5} ({oblig/total_oblig*100:5.2f}%) {total:<5} ({total/count*100:5.2f}%)")

if __name__ == "__main__":
	optimize()

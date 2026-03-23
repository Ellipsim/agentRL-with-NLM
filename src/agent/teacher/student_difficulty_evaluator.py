"""
> student_difficulty_evaluator.py

Difficulty reward for the NeSIG teacher combining two signals:

    r_total = 0.3 * max(LP, 0)  +  0.7 * difficulty_bonus

LP component (0.3 weight)
─────────────────────────
Tracks learning progress per num_blocks bucket using two EMAs.
Rewards the teacher when the student is genuinely improving on
problems of that block count.

    LP = fast_ema - slow_ema   (per num_blocks bucket)

Difficulty bonus (0.7 weight)
──────────────────────────────
Rewards the teacher for generating problems just above the student's
current frontier — the hardest num_blocks it currently handles reliably.
Uses a Gaussian centered at (frontier + margin) that fades on both sides:

    difficulty_bonus = gaussian(num_blocks, target=frontier + margin, sigma)

    too easy  (num_blocks << frontier)  → bonus ≈ 0
    at target (num_blocks ≈ frontier + margin) → bonus ≈ 1.0
    too hard  (num_blocks >> frontier)  → bonus ≈ 0  (fades past ceiling)

The frontier advances automatically as the student improves, so the
difficulty target always sits just ahead of the student's current level.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ─────────────────────────────────────────────────────────────────────
# LP tracker — one per num_blocks bucket
# ─────────────────────────────────────────────────────────────────────

@dataclass
class _LPTracker:
    """
    Tracks learning progress for one num_blocks bucket via two EMAs.

    fast_ema reacts in ~3 steps  (alpha=0.3)
    slow_ema reacts in ~20 steps (alpha=0.05)

    LP = fast_ema - slow_ema
        > 0  →  student is improving on this block count
        ≈ 0  →  student has plateaued
        < 0  →  student is regressing
    """
    alpha_fast: float = 0.3
    alpha_slow: float = 0.05

    _fast: Optional[float] = field(default=None, repr=False)
    _slow: Optional[float] = field(default=None, repr=False)
    _n:    int             = field(default=0,    repr=False)

    def update(self, outcome: float) -> float:
        """
        Feed a binary outcome (1.0 solved, 0.0 failed).
        Returns the current LP after the update.
        """
        if self._fast is None:
            self._fast = outcome
            self._slow = outcome
            self._n    = 1
            return 0.0  # need at least two observations for a delta

        self._fast = self.alpha_fast * outcome + (1 - self.alpha_fast) * self._fast
        self._slow = self.alpha_slow * outcome + (1 - self.alpha_slow) * self._slow
        self._n   += 1
        return self.lp

    @property
    def lp(self) -> float:
        if self._fast is None:
            return 0.0
        return self._fast - self._slow

    @property
    def success_rate(self) -> float:
        """Current competence estimate (fast EMA)."""
        return self._fast if self._fast is not None else 0.0

    @property
    def is_ready(self) -> bool:
        """Wait for at least 5 updates before trusting the LP signal."""
        return self._n >= 5


# ─────────────────────────────────────────────────────────────────────
# Frontier tracker
# ─────────────────────────────────────────────────────────────────────

class _FrontierTracker:
    """
    Tracks the student's current capability frontier — the hardest
    num_blocks the student handles reliably.

    Update rule:
        student solved a problem of N blocks  → frontier nudges toward N
        student failed a problem of N blocks  → frontier nudges toward N * 0.5

    This means the frontier converges to the num_blocks where the student
    succeeds roughly 50-70% of the time. It moves slowly (alpha=0.05) so
    it is not thrown off by individual episodes.
    """

    def __init__(self,
                 alpha:       float = 0.05,
                 min_blocks:  int   = 2,
                 max_blocks:  int   = 30):
        self.alpha      = alpha
        self.min_blocks = min_blocks
        self.max_blocks = max_blocks
        self._frontier: Optional[float] = None

    def update(self, num_blocks: int, goal_reached: bool) -> float:
        """
        Update the frontier given the outcome of one problem attempt.
        Returns the updated frontier value.
        """
        # On first call seed the frontier at the current block count
        if self._frontier is None:
            self._frontier = float(num_blocks)
            return self._frontier

        # Pull toward num_blocks on success, pull back on failure
        target = float(num_blocks) if goal_reached else num_blocks * 0.5
        self._frontier = (self.alpha * target
                          + (1 - self.alpha) * self._frontier)
        self._frontier = float(
            max(self.min_blocks, min(self.max_blocks, self._frontier))
        )
        return self._frontier

    @property
    def frontier(self) -> float:
        return self._frontier if self._frontier is not None else float(self.min_blocks)


# ─────────────────────────────────────────────────────────────────────
# Gaussian difficulty bonus
# ─────────────────────────────────────────────────────────────────────

def _gaussian_bonus(num_blocks: int,
                    target:     float,
                    sigma:      float = 2.0) -> float:
    """
    Reward that peaks when num_blocks == target and fades on both sides.

    sigma is in units of blocks (not a ratio), so sigma=2.0 means the
    reward is meaningful within ~2 blocks of the target in either direction.

    num_blocks << target  → bonus ≈ 0  (too easy)
    num_blocks == target  → bonus = 1.0
    num_blocks >> target  → bonus ≈ 0  (too hard, past ceiling)
    """
    return math.exp(-((num_blocks - target) ** 2) / (2 * sigma ** 2))


# ─────────────────────────────────────────────────────────────────────
# Main class
# ─────────────────────────────────────────────────────────────────────

class StudentDifficultyEvaluator:
    """
    Difficulty reward combining LP and a frontier-based difficulty bonus.

        r_total = w_lp * max(LP, 0)  +  w_diff * difficulty_bonus

    Parameters
    ----------
    max_actions : int
        Action budget (kept for interface compatibility).
    penalty : float
        Raw score for failed problems fed into the LP tracker.
        Default 0 — failure contributes no signal, not a punishment.
    alpha_fast : float
        EMA decay for the fast LP tracker (~3 step horizon).
    alpha_slow : float
        EMA decay for the slow LP tracker (~20 step horizon).
    frontier_alpha : float
        How fast the frontier moves. 0.05 = slow and stable.
    margin : float
        How many blocks above the frontier the target sits.
        Default 2 means the teacher is pushed toward problems
        2 blocks harder than what the student currently masters.
    sigma : float
        Width of the Gaussian in blocks. Default 2.0 means reward
        is significant within ~2 blocks of the target.
    w_lp : float
        Weight of the LP component.
    w_diff : float
        Weight of the difficulty bonus component.
    """

    def __init__(
        self,
        max_actions:    int,
        penalty:        float = 0.0,
        alpha_fast:     float = 0.3,
        alpha_slow:     float = 0.05,
        frontier_alpha: float = 0.05,
        margin:         float = 2.0,
        sigma:          float = 2.0,
        w_lp:           float = 0.3,
        w_diff:         float = 0.7,
    ):
        self.max_actions    = max_actions
        self.penalty        = penalty
        self.alpha_fast     = alpha_fast
        self.alpha_slow     = alpha_slow
        self.margin         = margin
        self.sigma          = sigma
        self.w_lp           = w_lp
        self.w_diff         = w_diff

        # One LP tracker per num_blocks value
        self._lp_trackers: Dict[int, _LPTracker] = {}

        # Single frontier tracker shared across all block counts
        self._frontier_tracker = _FrontierTracker(
            alpha=frontier_alpha,
            min_blocks=2,
            max_blocks=30,
        )

    def _get_lp_tracker(self, num_blocks: int) -> _LPTracker:
        if num_blocks not in self._lp_trackers:
            self._lp_trackers[num_blocks] = _LPTracker(
                alpha_fast=self.alpha_fast,
                alpha_slow=self.alpha_slow,
            )
        return self._lp_trackers[num_blocks]

    # ──────────────────────────────────────────────────────────────────
    # DifficultyEvaluator interface
    # ──────────────────────────────────────────────────────────────────

    def get_difficulty(self, problem_info_list: List[dict]) -> List[float]:
        """
        Compute teacher rewards for a batch of attempted problems.

        Args:
            problem_info_list: list of dicts from the student trainer.
                Required keys:
                    goal_reached (bool) — did the student solve it?
                    num_blocks   (int)  — number of blocks in the problem

        Returns:
            List of per-problem teacher rewards in [0, 1].
        """
        rewards = []

        for info in problem_info_list:
            num_blocks   = info['num_blocks']
            goal_reached = info['goal_reached']
            outcome      = 1.0 if goal_reached else 0.0

            # ── 1. Update frontier ───────────────────────────────────
            # Done before LP so the frontier reflects this outcome too
            self._frontier_tracker.update(num_blocks, goal_reached)
            frontier = self._frontier_tracker.frontier

            # ── 2. Update LP tracker for this num_blocks bucket ──────
            lp_tracker = self._get_lp_tracker(num_blocks)
            lp = lp_tracker.update(outcome)

            # ── 3. LP component ──────────────────────────────────────
            # max(LP, 0): only reward improvement, ignore plateau
            # Return 0 before tracker warms up to avoid noisy signal
            if not lp_tracker.is_ready:
                r_lp = 0.0
            else:
                r_lp = max(lp, 0.0)

            # ── 4. Difficulty bonus ──────────────────────────────────
            # Gaussian peaked at frontier + margin
            # Fades for problems too easy OR too hard
            target   = frontier + self.margin
            r_diff   = _gaussian_bonus(num_blocks, target, self.sigma)

            # ── 5. Combined reward ───────────────────────────────────
            reward = self.w_lp * r_lp + self.w_diff * r_diff
            rewards.append(reward)

        return rewards

    # ──────────────────────────────────────────────────────────────────
    # Diagnostics
    # ──────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        """
        Snapshot of internal state for TensorBoard logging.

        Usage in train_teacher_only.py:

            stats = difficulty_evaluator.summary()
            writer.add_scalar('Teacher/frontier',
                              stats['frontier'], global_step=current_step)
            writer.add_scalar('Teacher/target',
                              stats['target'],   global_step=current_step)
            for nb, s in stats['buckets'].items():
                writer.add_scalar(f'Teacher/LP_{nb}blocks',
                                  s['lp'], global_step=current_step)
                writer.add_scalar(f'Teacher/success_rate_{nb}blocks',
                                  s['success_rate'], global_step=current_step)
        """
        frontier = self._frontier_tracker.frontier
        target   = frontier + self.margin
        return {
            'frontier': frontier,
            'target':   target,
            'buckets':  {
                nb: {
                    'lp':          tracker.lp,
                    'success_rate': tracker.success_rate,
                    'n_updates':   tracker._n,
                    'ready':       tracker.is_ready,
                }
                for nb, tracker in sorted(self._lp_trackers.items())
            }
        }
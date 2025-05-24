import numpy as np

class MCDACalcAHP:
    def __init__(self, criteria, alternatives, criteria_matrix, alternatives_matrices):
        """
        Initialize AHP with decision problem parameters.
        
        Parameters:
        criteria (list): List of criterion names.
        alternatives (list): List of alternative names.
        criteria_matrix (list of lists): Pairwise comparison matrix for criteria.
        alternatives_matrices (list of lists of lists): List of pairwise comparison matrices for alternatives per criterion.
        """
        self.criteria = criteria
        self.alternatives = alternatives
        self.criteria_matrix = np.array(criteria_matrix)
        self.alternatives_matrices = [np.array(mat) for mat in alternatives_matrices]
        self.n_criteria = len(criteria)
        self.n_alternatives = len(alternatives)
        
    def _normalize_matrix(self, matrix):
        """Normalize a pairwise comparison matrix by column sums."""
        col_sums = matrix.sum(axis=0)
        col_sums[col_sums == 0] = 1 
        return matrix / col_sums
    
    def _compute_priority_vector(self, matrix):
        """Compute priority vector (weights) from a normalized matrix."""
        return np.mean(self._normalize_matrix(matrix), axis=1)
    
    def _consistency_ratio(self, matrix):
        """Compute consistency ratio for a pairwise comparison matrix."""
        n = matrix.shape[0]
        if n == 1:
            return 0.0
        priority_vector = self._compute_priority_vector(matrix)
        lambda_max = np.mean(np.sum(matrix @ priority_vector / priority_vector))
        ci = (lambda_max - n) / (n - 1)
        ri_values = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
        ri = ri_values.get(n, 1.49) 
        return ci / ri if ri > 0 else 0.0
    
    def compute_ahp(self, check_consistency=True, consistency_threshold=0.1):
        """
        Compute AHP priorities and optionally check consistency.
        
        Parameters:
        check_consistency (bool): If True, checks consistency ratio and raises error if above threshold.
        consistency_threshold (float): Maximum acceptable consistency ratio.
        
        Returns:
        tuple: (criteria_weights, alternative_scores, consistency_info)
        """
        criteria_cr = self._consistency_ratio(self.criteria_matrix)
        if check_consistency and criteria_cr > consistency_threshold:
            raise ValueError(f"Criteria matrix consistency ratio {criteria_cr:.3f} exceeds threshold {consistency_threshold}")
        
        criteria_weights = self._compute_priority_vector(self.criteria_matrix)
        
        alternatives_cr = [self._consistency_ratio(mat) for mat in self.alternatives_matrices]
        if check_consistency and any(cr > consistency_threshold for cr in alternatives_cr):
            raise ValueError(f"Alternatives matrix consistency ratio(s) {alternatives_cr} exceed threshold {consistency_threshold}")
        
        alternatives_priorities = [self._compute_priority_vector(mat) for mat in self.alternatives_matrices]
        
        alternative_scores = np.sum(np.array(alternatives_priorities).T * criteria_weights, axis=1)
        
        consistency_info = {
            "criteria_consistency_ratio": criteria_cr,
            "alternatives_consistency_ratios": alternatives_cr
        }
        
        return criteria_weights.tolist(), alternative_scores.tolist(), consistency_info